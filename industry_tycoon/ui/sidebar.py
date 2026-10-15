"""Sidebar: the current player's holdings, the leaderboard and game controls."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import catalog, rules
from industry_tycoon.game import Game
from industry_tycoon.player import Player
from industry_tycoon.ui import session
from industry_tycoon.ui.components import MONEY_COLUMN, format_counts


def render(game: Game) -> None:
    with st.sidebar:
        _render_holdings(game.current_player)
        st.divider()
        _render_leaderboard(game)
        st.divider()
        _render_new_game_control()


def _render_holdings(player: Player) -> None:
    st.subheader(f"{player.name} 的資產")
    st.markdown(
        "  \n".join(
            [
                f"**資源**：{format_counts(player.inventory, catalog.RESOURCES_BY_KEY)}",
                f"**待入帳產品**：{format_counts(player.pending_goods, catalog.RESOURCES_BY_KEY)}",
                f"**收集廠**：{format_counts(player.collection_plants, catalog.RESOURCES_BY_KEY)}",
                f"**加工廠**：{format_counts(player.processing_plants, catalog.RESOURCES_BY_KEY)}",
                f"**棋子**：{format_counts(player.pieces, catalog.PIECES_BY_KEY)}",
            ]
        )
    )


def _render_leaderboard(game: Game) -> None:
    st.subheader("總資產排行")
    ranking = sorted(game.players, key=game.market.net_worth, reverse=True)
    st.dataframe(
        [
            {
                "玩家": player.name,
                "總資產": game.market.net_worth(player),
                "狀態": _status(game, player),
            }
            for player in ranking
        ],
        hide_index=True,
        width="stretch",
        column_config={"總資產": MONEY_COLUMN},
    )


def _status(game: Game, player: Player) -> str:
    if player.eliminated:
        return "已淘汰"
    if player is game.current_player:
        return "行動中"
    if player.bankrupt_turns:
        return f"破產 {player.bankrupt_turns}/{rules.BANKRUPTCY_TURN_LIMIT}"
    return ""


def _render_new_game_control() -> None:
    with st.popover("開始新遊戲", icon="🔄", width="stretch"):
        st.write("目前的遊戲進度將會清除，確定要重新開始嗎？")
        st.button("確認重新開始", type="primary", key="confirm-new-game", on_click=session.end_game)
