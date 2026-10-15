from __future__ import annotations

import pytest

from industry_tycoon import catalog, rules
from industry_tycoon.errors import GameRuleError
from industry_tycoon.game import Game
from tests.conftest import GameFactory


class TestStart:
    def test_players_start_with_money_and_character_upkeep(self, make_game: GameFactory):
        game = make_game("edison", "cixi")

        assert [player.name for player in game.players] == ["P1", "P2"]
        assert all(player.money == rules.STARTING_MONEY for player in game.players)
        assert [player.upkeep for player in game.players] == [225, 0]
        assert game.current_player is game.players[0]
        assert game.round_number == 1

    @pytest.mark.parametrize("player_count", [1, 5])
    def test_rejects_unsupported_player_count(self, player_count: int):
        roster = [(f"P{seat}", catalog.CHARACTERS[0]) for seat in range(player_count)]
        with pytest.raises(GameRuleError):
            Game.start(roster)

    @pytest.mark.parametrize("names", [("Ann", "Ann"), ("Ann", " Ann "), ("Ann", "  ")])
    def test_rejects_duplicate_or_blank_names(self, names: tuple[str, str]):
        roster = [(name, catalog.CHARACTERS[0]) for name in names]
        with pytest.raises(GameRuleError):
            Game.start(roster)


class TestResources:
    def test_take_resource_adds_to_inventory(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        game.take_resource("wood")
        game.take_resource("wood", quantity=2)

        assert game.current_player.inventory["wood"] == 3

    def test_sell_applies_character_sale_multiplier(self, make_game: GameFactory):
        game = make_game("edison", "tesla")
        game.take_resource("wood", quantity=3)

        proceeds = game.sell("wood", 3)

        assert proceeds == 60 * 3 * 2
        assert game.current_player.money == rules.STARTING_MONEY + proceeds
        assert game.current_player.inventory["wood"] == 0

    def test_sell_more_than_owned_changes_nothing(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        game.take_resource("wood", quantity=2)

        with pytest.raises(GameRuleError):
            game.sell("wood", 3)

        assert game.current_player.inventory["wood"] == 2
        assert game.current_player.money == rules.STARTING_MONEY

    @pytest.mark.parametrize("quantity", [0, -5])
    def test_sell_rejects_non_positive_quantity(self, make_game: GameFactory, quantity: int):
        game = make_game("tesla", "tesla")

        with pytest.raises(GameRuleError):
            game.sell("wood", quantity)

        assert game.current_player.money == rules.STARTING_MONEY

    def test_sell_everything_applies_sale_multiplier(self, make_game: GameFactory):
        game = make_game("edison", "tesla")
        game.take_resource("wood", quantity=2)
        game.take_resource("gold")

        proceeds = game.sell_everything()

        assert proceeds == (60 * 2 + 600) * 2
        assert sum(game.current_player.inventory.values()) == 0

    def test_sell_everything_requires_holdings(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        with pytest.raises(GameRuleError):
            game.sell_everything()


class TestBuildings:
    def test_collection_plant_charges_its_cost(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        cost = game.build_collection_plant("wood")

        assert cost == 670
        assert game.current_player.money == rules.STARTING_MONEY - 670
        assert game.current_player.collection_plants["wood"] == 1

    @pytest.mark.parametrize(
        ("character", "expected_cost"), [("qin_shi_huang", 335), ("cixi", 603)]
    )
    def test_build_cost_modifiers_apply_once(
        self, make_game: GameFactory, character: str, expected_cost: int
    ):
        game = make_game(character, "tesla")

        assert game.build_collection_plant("wood") == expected_cost

    def test_unaffordable_plant_changes_nothing(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        with pytest.raises(GameRuleError, match="金錢不足"):
            game.build_collection_plant("gold")

        assert game.current_player.money == rules.STARTING_MONEY
        assert game.current_player.building_count == 0

    def test_per_player_building_limit(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        game.current_player.collection_plants["fish"] = rules.MAX_BUILDINGS_PER_PLAYER

        with pytest.raises(GameRuleError, match="每位玩家"):
            game.build_collection_plant("fish")

    def test_board_building_limit(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        game.players[0].collection_plants["fish"] = rules.MAX_BUILDINGS_ON_BOARD // 2
        game.players[1].collection_plants["fish"] = rules.MAX_BUILDINGS_ON_BOARD // 2

        with pytest.raises(GameRuleError, match="棋盤上"):
            game.build_collection_plant("fish")

    def test_processing_plant_charges_its_cost(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        assert game.build_processing_plant("fine_iron") == 950
        assert game.current_player.processing_plants["fine_iron"] == 1

    def test_destroy_collection_plant(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        target = game.players[1]
        target.collection_plants["wood"] = 1

        game.destroy_collection_plant(target, "wood")

        assert target.collection_plants["wood"] == 0

    def test_destroy_requires_an_existing_plant(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        with pytest.raises(GameRuleError):
            game.destroy_collection_plant(game.players[1], "wood")


class TestInvest:
    def test_requires_the_processing_plant(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        game.take_resource("iron_ore", quantity=3)

        with pytest.raises(GameRuleError, match="尚未擁有"):
            game.invest("fine_iron", {"iron_ore": 3})

        assert game.current_player.inventory["iron_ore"] == 3

    def test_output_is_delivered_when_the_turn_ends(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        investor = game.current_player
        investor.processing_plants["fine_iron"] = 1
        game.take_resource("iron_ore", quantity=3)

        units = game.invest("fine_iron", {"iron_ore": 3})

        assert units == round(160 * 3 * 2 / 320)
        assert investor.inventory["iron_ore"] == 0
        assert investor.inventory["fine_iron"] == 0
        assert investor.pending_goods["fine_iron"] == units

        game.end_turn()

        assert investor.inventory["fine_iron"] == units
        assert not investor.pending_goods

    def test_processed_output_multiplier_applies_on_delivery(self, make_game: GameFactory):
        game = make_game("edison", "tesla")
        investor = game.current_player
        investor.processing_plants["fine_iron"] = 1
        game.take_resource("iron_ore", quantity=3)

        game.invest("fine_iron", {"iron_ore": 3})
        game.end_turn()

        assert investor.inventory["fine_iron"] == round(3 * 1.75)

    @pytest.mark.parametrize("inputs", [{}, {"iron_ore": 0}, {"iron_ore": -1}])
    def test_rejects_empty_or_negative_inputs(self, make_game: GameFactory, inputs: dict):
        game = make_game("tesla", "tesla")
        game.current_player.processing_plants["fine_iron"] = 1

        with pytest.raises(GameRuleError):
            game.invest("fine_iron", inputs)

    def test_missing_input_changes_nothing(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        player = game.current_player
        player.processing_plants["food"] = 1
        game.take_resource("fish", quantity=2)
        game.take_resource("crop")

        with pytest.raises(GameRuleError, match="農作物不足"):
            game.invest("food", {"fish": 2, "crop": 5})

        assert player.inventory["fish"] == 2
        assert player.inventory["crop"] == 1


class TestPieces:
    def test_buying_charges_price_and_raises_upkeep(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        cost = game.buy_piece("castle")

        assert cost == 660
        assert game.current_player.pieces["castle"] == 1
        assert game.current_player.upkeep == 100 + rules.UPKEEP_PER_PIECE_BOUGHT

    def test_qin_shi_huang_pays_half(self, make_game: GameFactory):
        game = make_game("qin_shi_huang", "tesla")

        assert game.buy_piece("soldier") == 65

    def test_add_piece_is_free(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        game.add_piece("queen")

        assert game.current_player.pieces["queen"] == 1
        assert game.current_player.money == rules.STARTING_MONEY

    def test_capture_removes_the_piece_and_pays_the_bounty(self, make_game: GameFactory):
        game = make_game("genghis_khan", "tesla")
        target = game.players[1]
        target.pieces["knight"] = 1

        bounty = game.capture_piece(target, "knight")

        assert bounty == 175
        assert target.pieces["knight"] == 0
        assert game.current_player.money == rules.STARTING_MONEY + 175

    def test_capturing_an_untracked_starting_piece_still_pays(self, make_game: GameFactory):
        game = make_game("oppenheimer", "tesla")
        target = game.players[1]

        assert game.capture_piece(target, "king") == 50
        assert target.pieces["king"] == 0

    def test_buy_insurance(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        game.buy_insurance()

        assert game.current_player.money == rules.STARTING_MONEY - rules.INSURANCE_COST


class TestTurnFlow:
    def test_end_turn_charges_upkeep_and_moves_to_the_next_player(self, make_game: GameFactory):
        game = make_game("tesla", "edison")

        report = game.end_turn()

        assert game.players[0].money == rules.STARTING_MONEY - 100
        assert report.next_player is game.players[1]
        assert not report.started_new_round

    def test_upkeep_never_takes_money_below_zero(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        game.current_player.money = 50

        game.end_turn()

        assert game.players[0].money == 0

    def test_new_round_starts_after_the_last_seat(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")

        game.end_turn()
        report = game.end_turn()

        assert report.started_new_round
        assert game.round_number == 2
        assert game.current_player is game.players[0]

    def test_eliminated_players_are_skipped(self, make_game: GameFactory):
        game = make_game("tesla", "tesla", "tesla")
        game.set_eliminated(game.players[1], True)

        assert game.end_turn().next_player is game.players[2]

    def test_rounds_advance_when_the_first_seat_is_eliminated(self, make_game: GameFactory):
        game = make_game("tesla", "tesla", "tesla")
        game.set_eliminated(game.players[0], True)

        for _ in range(3):
            game.end_turn()

        assert game.round_number == 2
        assert game.current_player is game.players[1]

    def test_plant_output_uses_the_incoming_players_character(self, make_game: GameFactory):
        game = make_game("cixi", "tesla")
        cixi, tesla = game.players
        cixi.collection_plants["wood"] = 1
        tesla.collection_plants["wood"] = 1

        game.end_turn()  # Cixi -> Tesla
        game.end_turn()  # Tesla -> Cixi

        assert tesla.inventory["wood"] == 3
        assert cixi.inventory["wood"] == round(3 * 0.7)

    def test_ending_a_turn_with_everyone_eliminated_is_rejected(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        for player in game.players:
            game.set_eliminated(player, True)

        with pytest.raises(GameRuleError):
            game.end_turn()


class TestBankruptcy:
    def test_player_is_eliminated_after_consecutive_broke_turns(self, make_game: GameFactory):
        game = make_game("tesla", "tesla", "tesla")
        broke = game.players[1]
        broke.money = 0

        reports = [game.end_turn() for _ in range(3 * rules.BANKRUPTCY_TURN_LIMIT - 2)]

        assert broke.eliminated
        assert reports[-1].bankrupted == (broke,)
        assert reports[-1].next_player is game.players[2]

    def test_streak_resets_once_the_player_has_money(self, make_game: GameFactory):
        game = make_game("cixi", "cixi")  # Cixi has no upkeep.
        player = game.players[1]
        player.money = 0

        game.end_turn()
        assert player.bankrupt_turns == 1

        game.take_resource("wood")  # Still player 2's turn.
        game.sell("wood", 1)
        game.end_turn()

        assert player.bankrupt_turns == 0

    def test_last_player_standing_is_never_eliminated(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        game.set_eliminated(game.players[1], True)
        game.players[0].money = 0

        for _ in range(rules.BANKRUPTCY_TURN_LIMIT + 1):
            game.end_turn()

        assert not game.players[0].eliminated

    def test_reinstating_a_player_resets_their_streak(self, make_game: GameFactory):
        game = make_game("tesla", "tesla")
        player = game.players[1]
        player.bankrupt_turns = rules.BANKRUPTCY_TURN_LIMIT
        game.set_eliminated(player, True)

        game.set_eliminated(player, False)

        assert player.bankrupt_turns == 0
