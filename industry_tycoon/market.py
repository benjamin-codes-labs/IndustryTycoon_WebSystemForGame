"""Live, inflation-adjusted prices, character-specific quotes and asset valuation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from industry_tycoon import catalog, rules
from industry_tycoon.catalog import Character
from industry_tycoon.player import Player


def _scale(amount: float, multiplier: float) -> int:
    return round(amount * multiplier)


@dataclass
class Market:
    """Current prices of everything that can be bought, built or sold."""

    resource_prices: dict[str, int]
    collection_plant_costs: dict[str, int]
    processing_plant_costs: dict[str, int]
    piece_prices: dict[str, int]
    #: The multiplier applied to all prices at the start of the latest round.
    inflation_multiplier: float = 1.0
    #: Price level measured at the latest adjustment; ``None`` until the first one.
    last_price_level: float | None = None

    @classmethod
    def at_base_prices(cls) -> Market:
        return cls(
            resource_prices={item.key: item.price for item in catalog.RESOURCES},
            collection_plant_costs={item.key: item.plant_cost for item in catalog.RAW_RESOURCES},
            processing_plant_costs={item.key: item.plant_cost for item in catalog.PROCESSED_GOODS},
            piece_prices={
                item.key: item.price for item in catalog.PIECES if item.price is not None
            },
        )

    # --- Quotes adjusted for a character's modifiers -------------------------

    def sale_value(self, resource: str, quantity: int, character: Character) -> int:
        return _scale(self.resource_prices[resource] * quantity, character.sale_multiplier)

    def collection_plant_cost(self, resource: str, character: Character) -> int:
        return _scale(self.collection_plant_costs[resource], character.build_cost_multiplier)

    def processing_plant_cost(self, good: str, character: Character) -> int:
        return _scale(self.processing_plant_costs[good], character.build_cost_multiplier)

    def piece_cost(self, piece: str, character: Character) -> int:
        return _scale(self.piece_prices[piece], character.piece_cost_multiplier)

    def processing_yield(self, good: str, inputs: Mapping[str, int]) -> int:
        """Units of ``good`` produced by investing ``inputs`` into its processing plant."""
        input_value = sum(self.resource_prices[key] * quantity for key, quantity in inputs.items())
        output_value = input_value * catalog.PROCESSED_GOODS_BY_KEY[good].value_multiplier
        return round(output_value / self.resource_prices[good])

    # --- Valuation -----------------------------------------------------------

    def piece_value(self, piece: str) -> int:
        """Market value of a piece; synthesized pieces are worth the sum of their components."""
        spec = catalog.PIECES_BY_KEY[piece]
        if spec.is_purchasable:
            return self.piece_prices[piece]
        return sum(self.piece_value(component) for component in spec.components)

    def net_worth(self, player: Player) -> int:
        """Money plus the market value of every resource and piece the player holds."""
        resources = sum(
            self.resource_prices[key] * quantity for key, quantity in player.inventory.items()
        )
        pieces = sum(self.piece_value(key) * count for key, count in player.pieces.items())
        return player.money + resources + pieces

    # --- Inflation -----------------------------------------------------------

    def measure_price_level(self, players: Sequence[Player]) -> float:
        """Average weighted asset value per player: the "P" of the inflation model."""
        cash = sum(player.money for player in players)
        raw_resources = self.inflation_multiplier * sum(
            catalog.RAW_RESOURCES_BY_KEY[key].inflation_weight * quantity
            for player in players
            for key, quantity in player.inventory.items()
            if key in catalog.RAW_RESOURCES_BY_KEY
        )
        buildings = sum(player.building_count for player in players)
        pieces = sum(player.pieces.total() for player in players)
        total_assets = (
            cash
            + raw_resources
            + rules.BUILDING_ASSET_WEIGHT * buildings
            + rules.PIECE_ASSET_WEIGHT * pieces
        )
        return total_assets / len(players)

    def adjust_for_new_round(self, players: Sequence[Player], direction: int) -> None:
        """Reprice everything in proportion to how much the price level moved.

        ``direction`` is ``+1`` (prices follow the price level) or ``-1`` (prices
        move against it); the game picks it at random each round.
        """
        price_level = self.measure_price_level(players)
        if price_level <= 0:
            return  # Nothing to measure against while every player is broke.

        previous_level = (
            self.last_price_level
            if self.last_price_level is not None
            else price_level * rules.INITIAL_PRICE_LEVEL_RATIO
        )
        growth = (price_level - previous_level) / price_level
        multiplier = 1 + rules.INFLATION_SENSITIVITY * direction * growth

        for prices in (
            self.resource_prices,
            self.collection_plant_costs,
            self.processing_plant_costs,
            self.piece_prices,
        ):
            for key, price in prices.items():
                prices[key] = _scale(price, multiplier)

        self.inflation_multiplier = multiplier
        self.last_price_level = price_level
