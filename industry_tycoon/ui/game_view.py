"""Main game screen: turn header, current player's status and the action tabs."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import rules
from industry_tycoon.formatting import money
from industry_tycoon.game import Game
from industry_tycoon.ui import session, sidebar
from industry_tycoon.ui.components import describe_character
from industry_tycoon.ui.tabs import conflict, market, pieces, processing, resources

#: Widgets holding per-turn input that should not carry over to the next player.
_PER_TURN_WIDGET_PREFIXES = (market.WIDGET_PREFIX, processing.WIDGET_PREFIX)


def render(game: Game) -> None:
    sidebar.render(game)
    _render_header(game)

    tabs = st.tabs(["📦 原料與收集廠", "🏭 加工廠", "💰 市場", "♟️ 棋子與保險", "⚔️ 對戰與淘汰"])
    for tab, module in zip(tabs, (resources, processing, market, pieces, conflict), strict=True):
        with tab:
            module.render(game)


def _render_header(game: Game) -> None:
    player = game.current_player
    character = player.character

    st.title(f"第 {game.round_number} 回合")
    st.subheader(f"輪到 {player.name}（{character.label}）")
    st.caption(describe_character(character))

    columns = st.columns(5, vertical_alignment="bottom")
    columns[0].metric("金錢", money(player.money))
    columns[1].metric("每回合支出", money(player.upkeep))
    columns[2].metric(
        "建築",
        f"{player.building_count} / {rules.MAX_BUILDINGS_PER_PLAYER}",
        help=f"棋盤上共 {game.buildings_on_board} / {rules.MAX_BUILDINGS_ON_BOARD} 座",
    )

    multiplier = game.market.inflation_multiplier
    columns[3].metric(
        "通貨膨脹率",
        f"×{multiplier:.3f}",
        delta=f"{multiplier - 1:+.2%}" if multiplier != 1 else None,
        delta_color="off",
        help="每回合開始時，所有價格都會乘以此倍率。",
    )
    columns[4].button(
        "下一位玩家",
        icon="➡️",
        type="primary",
        width="stretch",
        key="end-turn",
        on_click=session.perform,
        args=(_end_turn, game),
    )


def _end_turn(game: Game) -> str:
    report = game.end_turn()
    session.reset_widgets(*_PER_TURN_WIDGET_PREFIXES)

    for player in report.bankrupted:
        session.notify(
            f"{player.name} 連續 {rules.BANKRUPTCY_TURN_LIMIT} 回合破產，已被淘汰", icon="💸"
        )
    if report.started_new_round:
        multiplier = game.market.inflation_multiplier
        session.notify(f"第 {game.round_number} 回合開始，物價 ×{multiplier:.3f}", icon="📈")
    return f"輪到 {report.next_player.name}"
