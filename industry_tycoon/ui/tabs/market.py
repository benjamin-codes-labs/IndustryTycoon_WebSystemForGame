"""Market: current prices and selling resources."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import catalog
from industry_tycoon.formatting import money
from industry_tycoon.game import Game
from industry_tycoon.ui.components import MONEY_COLUMN
from industry_tycoon.ui.session import perform

WIDGET_PREFIX = "sell-"
_RESOURCE_KEY = f"{WIDGET_PREFIX}resource"
_QUANTITY_KEY = f"{WIDGET_PREFIX}quantity"


def render(game: Game) -> None:
    prices_column, actions_column = st.columns([3, 2], gap="large")
    with prices_column:
        _render_price_table(game)
    with actions_column:
        _render_sell_form(game)
        _render_sell_everything(game)


def _render_price_table(game: Game) -> None:
    player = game.current_player
    st.dataframe(
        [
            {
                "資源": resource.label,
                "類別": "原料" if resource.key in catalog.RAW_RESOURCES_BY_KEY else "加工品",
                "售價": game.market.resource_prices[resource.key],
                "持有": player.inventory[resource.key],
                "全部賣出可得": game.market.sale_value(
                    resource.key, player.inventory[resource.key], player.character
                ),
            }
            for resource in catalog.RESOURCES
        ],
        hide_index=True,
        width="stretch",
        column_config={"售價": MONEY_COLUMN, "全部賣出可得": MONEY_COLUMN},
    )


def _render_sell_form(game: Game) -> None:
    player = game.current_player
    with st.container(border=True):
        st.markdown("**出售資源**")
        resource = st.selectbox(
            "資源",
            list(catalog.RESOURCES_BY_KEY),
            format_func=lambda key: catalog.RESOURCES_BY_KEY[key].label,
            key=_RESOURCE_KEY,
        )
        assert resource is not None  # Selectboxes default to the first option.
        quantity = st.number_input("數量", min_value=0, step=1, key=_QUANTITY_KEY)
        proceeds = game.market.sale_value(resource, quantity, player.character)
        st.caption(f"持有 {player.inventory[resource]}・預計收入 {money(proceeds)}")
        st.button(
            "賣出",
            type="primary",
            width="stretch",
            key="sell-submit",
            on_click=perform,
            args=(_sell, game),
        )


def _render_sell_everything(game: Game) -> None:
    player = game.current_player
    total = sum(
        game.market.sale_value(key, quantity, player.character)
        for key, quantity in player.inventory.items()
    )
    with st.container(border=True):
        st.markdown("**全部資源售賣**")
        st.caption(f"以目前價格賣出所有資源，預計收入 {money(total)}")
        st.button(
            "全部賣出",
            width="stretch",
            key="sell-everything",
            on_click=perform,
            args=(_sell_everything, game),
        )


def _sell(game: Game) -> str:
    resource = st.session_state[_RESOURCE_KEY]
    quantity = st.session_state[_QUANTITY_KEY]
    proceeds = game.sell(resource, quantity)
    st.session_state[_QUANTITY_KEY] = 0
    return f"賣出 {catalog.RESOURCES_BY_KEY[resource].label} ×{quantity}，獲得 {money(proceeds)}"


def _sell_everything(game: Game) -> str:
    proceeds = game.sell_everything()
    return f"已賣出所有資源，獲得 {money(proceeds)}"
