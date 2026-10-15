from __future__ import annotations

import pytest

from industry_tycoon import catalog, rules
from industry_tycoon.market import Market
from industry_tycoon.player import Player


def _player(money: int = rules.STARTING_MONEY) -> Player:
    player = Player("P", catalog.CHARACTERS_BY_KEY["tesla"])
    player.money = money
    return player


def test_market_opens_at_catalog_prices():
    market = Market.at_base_prices()

    assert market.resource_prices["wood"] == 60
    assert market.resource_prices["steel"] == 840
    assert market.collection_plant_costs["gold"] == 2400
    assert market.processing_plant_costs["gasoline"] == 2300
    assert market.piece_prices == {"castle": 660, "bishop": 400, "knight": 400, "soldier": 130}
    assert market.inflation_multiplier == 1.0


class TestValuation:
    def test_synthesized_pieces_are_worth_their_components(self):
        market = Market.at_base_prices()

        assert market.piece_value("queen") == 400 + 660
        assert market.piece_value("general") == 660 + 400
        assert market.piece_value("king") == 0

    def test_net_worth_counts_money_resources_and_pieces(self):
        market = Market.at_base_prices()
        player = _player(money=1000)
        player.inventory.update({"wood": 2, "steel": 1})
        player.pieces.update({"knight": 1, "queen": 2})

        assert market.net_worth(player) == 1000 + 2 * 60 + 840 + 400 + 2 * 1060

    def test_processing_yield_scales_input_value(self):
        market = Market.at_base_prices()

        units = market.processing_yield("steel", {"fine_iron": 2, "coal": 3})

        assert units == round((2 * 320 + 3 * 120) * 3 / 840)


class TestInflation:
    def test_price_level_weighs_raw_resources_buildings_and_pieces(self):
        market = Market.at_base_prices()
        rich, other = _player(), _player()
        rich.inventory.update({"wood": 4, "fine_iron": 5})  # Processed goods are not weighed.
        rich.collection_plants["wood"] = 1
        rich.pieces["soldier"] = 1

        expected_total = (
            2 * rules.STARTING_MONEY
            + 4 * 25
            + rules.BUILDING_ASSET_WEIGHT
            + rules.PIECE_ASSET_WEIGHT
        )
        assert market.measure_price_level([rich, other]) == expected_total / 2

    @pytest.mark.parametrize(
        ("direction", "expected_multiplier", "expected_wood_price"), [(1, 1.01, 61), (-1, 0.99, 59)]
    )
    def test_first_round_assumes_five_percent_growth(
        self, direction: int, expected_multiplier: float, expected_wood_price: int
    ):
        market = Market.at_base_prices()

        market.adjust_for_new_round([_player(), _player()], direction)

        assert market.inflation_multiplier == pytest.approx(expected_multiplier)
        assert market.resource_prices["wood"] == expected_wood_price
        assert market.last_price_level == rules.STARTING_MONEY

    def test_later_rounds_compare_against_the_recorded_level(self):
        market = Market.at_base_prices()
        players = [_player(), _player()]
        market.adjust_for_new_round(players, direction=1)
        players[0].money = 3000

        market.adjust_for_new_round(players, direction=1)

        level = (3000 + rules.STARTING_MONEY) / 2
        growth = (level - rules.STARTING_MONEY) / level
        assert market.inflation_multiplier == pytest.approx(
            1 + rules.INFLATION_SENSITIVITY * growth
        )

    def test_inflation_reprices_everything(self):
        market = Market.at_base_prices()

        market.adjust_for_new_round([_player(), _player()], direction=1)

        assert market.collection_plant_costs["wood"] == round(670 * 1.01)
        assert market.processing_plant_costs["steel"] == round(2510 * 1.01)
        assert market.piece_prices["castle"] == round(660 * 1.01)

    def test_prices_hold_while_everyone_is_broke(self):
        market = Market.at_base_prices()

        market.adjust_for_new_round([_player(money=0), _player(money=0)], direction=1)

        assert market == Market.at_base_prices()
