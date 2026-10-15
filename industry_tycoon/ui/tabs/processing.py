"""Processing plants: build them and invest raw resources for higher-value goods."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import catalog
from industry_tycoon.catalog import ProcessedGood
from industry_tycoon.formatting import money
from industry_tycoon.game import Game
from industry_tycoon.ui.components import grid
from industry_tycoon.ui.session import perform

WIDGET_PREFIX = "invest-"


def render(game: Game) -> None:
    st.caption("先建造加工廠，再投入原料換取更高價值的產品；產品會在本回合結束時入帳。")
    for column, good in grid(catalog.PROCESSED_GOODS, columns=5):
        with column.container(border=True):
            _render_plant(game, good)


def _render_plant(game: Game, good: ProcessedGood) -> None:
    player = game.current_player
    plants_owned = player.processing_plants[good.key]
    plant_cost = game.market.processing_plant_cost(good.key, player.character)

    st.markdown(f"**{good.plant_label}**")
    st.caption(
        f"建造成本 {money(plant_cost)}・已建 {plants_owned} 座  \n"
        f"產品：{good.label}（售價 {money(game.market.resource_prices[good.key])}）"
    )
    st.button(
        "建造加工廠",
        key=f"build-processing-{good.key}",
        width="stretch",
        on_click=perform,
        args=(_build_plant, game, good),
    )

    inputs = {
        key: st.number_input(
            f"投入{catalog.RESOURCES_BY_KEY[key].label}（持有 {player.inventory[key]}）",
            min_value=0,
            step=1,
            key=_input_key(good, key),
        )
        for key in good.inputs
    }
    st.caption(f"預計產出：{good.label} ×{game.market.processing_yield(good.key, inputs)}")
    st.button(
        "投入資源",
        key=f"invest-submit-{good.key}",
        width="stretch",
        disabled=not plants_owned,
        help=None if plants_owned else f"需先建造{good.plant_label}",
        on_click=perform,
        args=(_invest, game, good),
    )


def _input_key(good: ProcessedGood, resource: str) -> str:
    return f"{WIDGET_PREFIX}{good.key}-{resource}"


def _build_plant(game: Game, good: ProcessedGood) -> str:
    cost = game.build_processing_plant(good.key)
    return f"建造了{good.plant_label}，花費 {money(cost)}"


def _invest(game: Game, good: ProcessedGood) -> str:
    inputs = {key: st.session_state[_input_key(good, key)] for key in good.inputs}
    units = game.invest(good.key, inputs)
    for key in good.inputs:
        st.session_state[_input_key(good, key)] = 0
    return f"投入成功：{good.label} ×{units} 將於回合結束時入帳"
