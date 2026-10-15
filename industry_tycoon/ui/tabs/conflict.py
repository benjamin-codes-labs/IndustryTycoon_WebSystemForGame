"""Conflict: destroy buildings, capture pieces and manage eliminations."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import catalog, rules
from industry_tycoon.formatting import money
from industry_tycoon.game import Game
from industry_tycoon.ui.session import perform

_PLANT_OWNER_KEY = "destroy-plant-owner"
_PLANT_RESOURCE_KEY = "destroy-plant-resource"
_PIECE_OWNER_KEY = "capture-piece-owner"
_PIECE_KEY = "capture-piece"


def render(game: Game) -> None:
    plant_column, piece_column, status_column = st.columns(3, gap="large")
    with plant_column, st.container(border=True):
        _render_destroy_plant(game)
    with piece_column, st.container(border=True):
        _render_capture_piece(game)
    with status_column, st.container(border=True):
        _render_eliminations(game)


def _player_selectbox(game: Game, label: str, key: str) -> None:
    st.selectbox(
        label,
        range(len(game.players)),
        format_func=lambda index: game.players[index].name,
        key=key,
    )


def _render_destroy_plant(game: Game) -> None:
    st.markdown("**摧毀收集廠**")
    _player_selectbox(game, "目標玩家", _PLANT_OWNER_KEY)
    st.selectbox(
        "目標收集廠",
        list(catalog.RAW_RESOURCES_BY_KEY),
        format_func=lambda key: catalog.RAW_RESOURCES_BY_KEY[key].label,
        key=_PLANT_RESOURCE_KEY,
    )
    st.button(
        "摧毀收集廠",
        width="stretch",
        key="destroy-plant-submit",
        on_click=perform,
        args=(_destroy_plant, game),
    )


def _render_capture_piece(game: Game) -> None:
    st.markdown("**擊殺棋子**")
    _player_selectbox(game, "目標玩家", _PIECE_OWNER_KEY)
    st.selectbox(
        "目標棋子",
        list(catalog.PIECES_BY_KEY),
        format_func=lambda key: catalog.PIECES_BY_KEY[key].label,
        key=_PIECE_KEY,
    )
    st.button(
        "擊殺棋子",
        width="stretch",
        key="capture-piece-submit",
        on_click=perform,
        args=(_capture_piece, game),
    )


def _render_eliminations(game: Game) -> None:
    st.markdown("**淘汰狀態**")
    st.caption(f"國王被消滅時勾選；連續 {rules.BANKRUPTCY_TURN_LIMIT} 回合破產會自動淘汰。")
    for index, player in enumerate(game.players):
        key = f"eliminated-{index}"
        # The game state is authoritative: it can change without this widget being touched.
        st.session_state[key] = player.eliminated
        st.checkbox(
            f"{player.name} 已淘汰",
            key=key,
            on_change=perform,
            args=(_toggle_elimination, game, index, key),
        )


def _destroy_plant(game: Game) -> str:
    owner = game.players[st.session_state[_PLANT_OWNER_KEY]]
    resource = st.session_state[_PLANT_RESOURCE_KEY]
    game.destroy_collection_plant(owner, resource)
    return f"已摧毀 {owner.name} 的{catalog.RAW_RESOURCES_BY_KEY[resource].label}收集廠"


def _capture_piece(game: Game) -> str:
    owner = game.players[st.session_state[_PIECE_OWNER_KEY]]
    piece = st.session_state[_PIECE_KEY]
    bounty = game.capture_piece(owner, piece)
    message = f"已擊殺 {owner.name} 的{catalog.PIECES_BY_KEY[piece].label}"
    return f"{message}，獲得獎勵 {money(bounty)}" if bounty else message


def _toggle_elimination(game: Game, index: int, key: str) -> str:
    player = game.players[index]
    eliminated = st.session_state[key]
    game.set_eliminated(player, eliminated)
    return f"{player.name} 已被淘汰" if eliminated else f"{player.name} 已恢復參賽"
