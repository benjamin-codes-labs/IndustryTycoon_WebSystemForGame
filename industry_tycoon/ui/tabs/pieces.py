"""Pieces and insurance: buy pieces, record synthesized ones and buy insurance."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import catalog, rules
from industry_tycoon.catalog import Piece
from industry_tycoon.formatting import money
from industry_tycoon.game import Game
from industry_tycoon.ui.components import grid
from industry_tycoon.ui.session import perform

_PURCHASABLE = [piece for piece in catalog.PIECES if piece.is_purchasable]
_SYNTHESIZED = [piece for piece in catalog.PIECES if not piece.is_purchasable]


def render(game: Game) -> None:
    st.markdown("##### 購買棋子")
    st.caption(f"每購買一隻棋子，每回合支出增加 {money(rules.UPKEEP_PER_PIECE_BOUGHT)}。")
    for column, piece in grid(_PURCHASABLE, columns=4):
        with column.container(border=True):
            _render_purchasable(game, piece)

    st.markdown("##### 合成棋子")
    st.caption("在棋盤上合成或獲得以下棋子後，於此記錄。")
    for column, piece in grid(_SYNTHESIZED, columns=4):
        with column.container(border=True):
            _render_synthesized(game, piece)

    st.markdown("##### 保險")
    with st.container(border=True):
        st.caption("保護一名玩家的建築與棋子至本回合結束（攻擊國王時除外）。")
        st.button(
            f"購買保險（{money(rules.INSURANCE_COST)}）",
            key="buy-insurance",
            on_click=perform,
            args=(_buy_insurance, game),
        )


def _render_purchasable(game: Game, piece: Piece) -> None:
    player = game.current_player
    cost = game.market.piece_cost(piece.key, player.character)
    st.markdown(f"**{piece.label}**")
    st.caption(f"價格 {money(cost)}・持有 {player.pieces[piece.key]}")
    st.button(
        f"購買{piece.label}",
        key=f"buy-piece-{piece.key}",
        width="stretch",
        on_click=perform,
        args=(_buy, game, piece),
    )


def _render_synthesized(game: Game, piece: Piece) -> None:
    player = game.current_player
    if piece.components:
        recipe = " + ".join(catalog.PIECES_BY_KEY[key].label for key in piece.components)
    else:
        recipe = "無法購買或合成"
    st.markdown(f"**{piece.label}**")
    st.caption(f"{recipe}・持有 {player.pieces[piece.key]}")
    st.button(
        f"記錄獲得{piece.label}",
        key=f"add-piece-{piece.key}",
        width="stretch",
        on_click=perform,
        args=(_add, game, piece),
    )


def _buy(game: Game, piece: Piece) -> str:
    cost = game.buy_piece(piece.key)
    return f"購買了{piece.label}，花費 {money(cost)}"


def _add(game: Game, piece: Piece) -> str:
    game.add_piece(piece.key)
    return f"已記錄獲得{piece.label}"


def _buy_insurance(game: Game) -> str:
    cost = game.buy_insurance()
    return f"已購買保險，花費 {money(cost)}"
