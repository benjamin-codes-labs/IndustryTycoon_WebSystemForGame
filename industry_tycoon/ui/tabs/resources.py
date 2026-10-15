"""Raw resources: take resources from cards and build collection plants."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import catalog
from industry_tycoon.catalog import RawResource
from industry_tycoon.formatting import money
from industry_tycoon.game import Game
from industry_tycoon.ui.components import grid
from industry_tycoon.ui.session import perform


def render(game: Game) -> None:
    st.caption("抽到資源卡時拿取原料；收集廠會在擁有者每回合開始時自動產出原料。")
    for column, resource in grid(catalog.RAW_RESOURCES, columns=5):
        with column.container(border=True):
            _render_resource(game, resource)


def _render_resource(game: Game, resource: RawResource) -> None:
    player = game.current_player
    plant_cost = game.market.collection_plant_cost(resource.key, player.character)

    st.markdown(f"**{resource.label}**")
    st.caption(
        f"售價 {money(game.market.resource_prices[resource.key])}・持有 "
        f"{player.inventory[resource.key]}  \n"
        f"收集廠 {money(plant_cost)}・已建 {player.collection_plants[resource.key]} 座  \n"
        f"每座每回合產出 {resource.output_per_plant}"
    )
    st.button(
        "拿取 ×1",
        key=f"take-{resource.key}",
        width="stretch",
        on_click=perform,
        args=(_take, game, resource),
    )
    st.button(
        "建造收集廠",
        key=f"build-collection-{resource.key}",
        width="stretch",
        on_click=perform,
        args=(_build_plant, game, resource),
    )


def _take(game: Game, resource: RawResource) -> str:
    game.take_resource(resource.key)
    return f"拿取了 1 個{resource.label}"


def _build_plant(game: Game, resource: RawResource) -> str:
    cost = game.build_collection_plant(resource.key)
    return f"建造了{resource.label}收集廠，花費 {money(cost)}"
