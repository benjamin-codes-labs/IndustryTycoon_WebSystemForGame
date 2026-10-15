"""The game aggregate: turn order, player actions and end-of-turn bookkeeping."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from industry_tycoon import catalog, rules
from industry_tycoon.catalog import Character
from industry_tycoon.errors import GameRuleError
from industry_tycoon.market import Market
from industry_tycoon.player import Player


@dataclass(frozen=True)
class TurnReport:
    """What happened while the turn was handed to the next player."""

    next_player: Player
    started_new_round: bool
    bankrupted: tuple[Player, ...] = ()


@dataclass
class Game:
    """A game in progress.

    Actions without an explicit ``owner`` apply to the player whose turn it
    is. Every action either completes fully or raises :class:`GameRuleError`
    without changing any state.
    """

    players: list[Player]
    market: Market = field(default_factory=Market.at_base_prices)
    round_number: int = 1
    current_index: int = 0
    rng: random.Random = field(default_factory=random.Random, repr=False, compare=False)

    @classmethod
    def start(
        cls, roster: Sequence[tuple[str, Character]], *, rng: random.Random | None = None
    ) -> Game:
        """Create a game from ``(name, character)`` pairs, in turn order."""
        if not rules.MIN_PLAYERS <= len(roster) <= rules.MAX_PLAYERS:
            raise GameRuleError(f"玩家人數必須介於 {rules.MIN_PLAYERS} 至 {rules.MAX_PLAYERS} 人")

        names = [name.strip() for name, _ in roster]
        if not all(names):
            raise GameRuleError("玩家名稱不能空白")
        if len(set(names)) != len(names):
            raise GameRuleError("玩家名稱不能重複")

        players = [
            Player(name, character) for name, (_, character) in zip(names, roster, strict=True)
        ]
        return cls(players=players, rng=rng or random.Random())

    # --- Queries -------------------------------------------------------------

    @property
    def current_player(self) -> Player:
        return self.players[self.current_index]

    @property
    def active_players(self) -> list[Player]:
        return [player for player in self.players if not player.eliminated]

    @property
    def buildings_on_board(self) -> int:
        return sum(player.building_count for player in self.players)

    # --- Resources -----------------------------------------------------------

    def take_resource(self, resource: str, quantity: int = 1) -> None:
        """Add resources drawn from a card to the current player's inventory."""
        _require_positive(quantity)
        self.current_player.inventory[resource] += quantity

    def sell(self, resource: str, quantity: int) -> int:
        """Sell resources at the current price; returns the money received."""
        _require_positive(quantity)
        player = self.current_player
        player.consume({resource: quantity})
        proceeds = self.market.sale_value(resource, quantity, player.character)
        player.money += proceeds
        return proceeds

    def sell_everything(self) -> int:
        """Sell the current player's entire inventory; returns the money received."""
        holdings = {key: qty for key, qty in self.current_player.inventory.items() if qty > 0}
        if not holdings:
            raise GameRuleError("沒有可出售的資源")
        return sum(self.sell(key, quantity) for key, quantity in holdings.items())

    # --- Buildings -----------------------------------------------------------

    def build_collection_plant(self, resource: str) -> int:
        """Build a collection plant for a raw resource; returns the cost paid."""
        player = self.current_player
        self._ensure_building_capacity(player)
        cost = self.market.collection_plant_cost(resource, player.character)
        player.pay(cost)
        player.collection_plants[resource] += 1
        return cost

    def build_processing_plant(self, good: str) -> int:
        """Build a processing plant for a processed good; returns the cost paid."""
        player = self.current_player
        self._ensure_building_capacity(player)
        cost = self.market.processing_plant_cost(good, player.character)
        player.pay(cost)
        player.processing_plants[good] += 1
        return cost

    def invest(self, good: str, inputs: Mapping[str, int]) -> int:
        """Feed resources into a processing plant.

        The output is queued and delivered when the current turn ends. Returns
        the number of units queued.
        """
        player = self.current_player
        spec = catalog.PROCESSED_GOODS_BY_KEY[good]
        if not player.processing_plants[good]:
            raise GameRuleError(f"尚未擁有{spec.plant_label}")

        invested = {key: quantity for key, quantity in inputs.items() if quantity}
        if not invested:
            raise GameRuleError("請輸入要投入的資源數量")
        for key, quantity in invested.items():
            if key not in spec.inputs:
                raise ValueError(f"{key!r} is not an input of {good!r}")
            _require_positive(quantity)

        player.consume(invested)
        units = self.market.processing_yield(good, invested)
        player.pending_goods[good] += units
        return units

    def destroy_collection_plant(self, owner: Player, resource: str) -> None:
        if not owner.collection_plants[resource]:
            label = catalog.RAW_RESOURCES_BY_KEY[resource].label
            raise GameRuleError(f"{owner.name} 沒有{label}收集廠")
        owner.collection_plants[resource] -= 1

    # --- Pieces --------------------------------------------------------------

    def buy_piece(self, piece: str) -> int:
        """Buy a piece; each purchase also raises the buyer's upkeep. Returns the cost paid."""
        player = self.current_player
        cost = self.market.piece_cost(piece, player.character)
        player.pay(cost)
        player.pieces[piece] += 1
        player.upkeep += rules.UPKEEP_PER_PIECE_BOUGHT
        return cost

    def add_piece(self, piece: str) -> None:
        """Record a piece obtained without paying, e.g. by synthesis."""
        self.current_player.pieces[piece] += 1

    def capture_piece(self, owner: Player, piece: str) -> int:
        """Record that the current player captured ``owner``'s piece; returns the bounty paid."""
        # Starting pieces are not tracked by the app, so capturing one can't lower the tally.
        if owner.pieces[piece] > 0:
            owner.pieces[piece] -= 1
        bounty = self.current_player.character.capture_bounty
        self.current_player.money += bounty
        return bounty

    def buy_insurance(self) -> int:
        self.current_player.pay(rules.INSURANCE_COST)
        return rules.INSURANCE_COST

    # --- Turn flow -----------------------------------------------------------

    def set_eliminated(self, player: Player, eliminated: bool) -> None:
        player.eliminated = eliminated
        if not eliminated:
            player.bankrupt_turns = 0

    def end_turn(self) -> TurnReport:
        """Settle the current player's turn and hand over to the next active player.

        The outgoing player pays upkeep and receives the goods they processed.
        Moving past the last seat starts a new round, which reprices the market.
        The incoming player is checked for bankruptcy, then collects the output
        of their collection plants.
        """
        if not self.active_players:
            raise GameRuleError("所有玩家均已淘汰")

        self._settle_turn(self.current_player)

        started_new_round = False
        bankrupted: list[Player] = []
        while True:
            started_new_round |= self._advance_to_next_active_player()
            if not self._eliminate_if_bankrupt(self.current_player):
                break
            bankrupted.append(self.current_player)

        self._collect_plant_output(self.current_player)
        return TurnReport(self.current_player, started_new_round, tuple(bankrupted))

    # --- Internals -----------------------------------------------------------

    def _ensure_building_capacity(self, player: Player) -> None:
        if player.building_count >= rules.MAX_BUILDINGS_PER_PLAYER:
            raise GameRuleError(f"每位玩家最多只能擁有 {rules.MAX_BUILDINGS_PER_PLAYER} 座建築")
        if self.buildings_on_board >= rules.MAX_BUILDINGS_ON_BOARD:
            raise GameRuleError(f"棋盤上最多只能有 {rules.MAX_BUILDINGS_ON_BOARD} 座建築")

    @staticmethod
    def _settle_turn(player: Player) -> None:
        if player.money > 0:
            player.bankrupt_turns = 0
        player.money = max(0, player.money - player.upkeep)

        multiplier = player.character.processed_output_multiplier
        for good, units in player.pending_goods.items():
            player.inventory[good] += round(units * multiplier)
        player.pending_goods.clear()

    def _advance_to_next_active_player(self) -> bool:
        """Move to the next active seat; returns whether a new round started."""
        seat_count = len(self.players)
        seats_in_turn_order = (
            (self.current_index + step) % seat_count for step in range(1, seat_count + 1)
        )
        index = next(seat for seat in seats_in_turn_order if not self.players[seat].eliminated)

        started_new_round = index <= self.current_index
        self.current_index = index
        if started_new_round:
            self.round_number += 1
            self.market.adjust_for_new_round(self.players, direction=self.rng.choice((1, -1)))
        return started_new_round

    def _eliminate_if_bankrupt(self, player: Player) -> bool:
        """Track a player's bankruptcy streak; returns whether they were just eliminated."""
        if player.money > 0:
            player.bankrupt_turns = 0
            return False

        player.bankrupt_turns += 1
        # The last player standing has won and can't be eliminated.
        if player.bankrupt_turns < rules.BANKRUPTCY_TURN_LIMIT or len(self.active_players) == 1:
            return False

        player.eliminated = True
        return True

    @staticmethod
    def _collect_plant_output(player: Player) -> None:
        multiplier = player.character.collection_output_multiplier
        for resource, plants in player.collection_plants.items():
            output = plants * catalog.RAW_RESOURCES_BY_KEY[resource].output_per_plant
            player.inventory[resource] += round(output * multiplier)


def _require_positive(quantity: int) -> None:
    if quantity <= 0:
        raise GameRuleError("數量必須大於 0")
