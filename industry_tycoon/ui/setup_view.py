"""Pre-game setup: number of players, their names and characters."""

from __future__ import annotations

import streamlit as st

from industry_tycoon import catalog, rules
from industry_tycoon.catalog import Character
from industry_tycoon.game import Game
from industry_tycoon.ui import session
from industry_tycoon.ui.components import MONEY_COLUMN, describe_character

_PLAYER_COUNTS = list(range(rules.MIN_PLAYERS, rules.MAX_PLAYERS + 1))
_PLAYER_COUNT_KEY = "setup-player-count"


def render() -> None:
    st.title("🏭 Industry Tycoon")
    st.caption("桌遊《Industry Tycoon》配套記帳系統：自動計算金錢、資源、建築、棋子與通貨膨脹。")

    st.subheader("遊戲設定")
    player_count = st.radio(
        "玩家人數",
        _PLAYER_COUNTS,
        index=len(_PLAYER_COUNTS) - 1,
        horizontal=True,
        format_func=lambda count: f"{count} 人",
        key=_PLAYER_COUNT_KEY,
    )
    assert player_count is not None  # A default index is set, so an option is always selected.

    with st.form("setup-form", border=True):
        for seat in range(1, player_count + 1):
            _render_seat(seat)
        st.form_submit_button(
            "開始遊戲",
            type="primary",
            key="start-game",
            on_click=session.perform,
            args=(_start_game,),
        )

    with st.expander("角色能力一覽"):
        _render_character_reference()


def _render_seat(seat: int) -> None:
    name_column, character_column = st.columns(2)
    name_column.text_input(
        f"玩家 {seat} 名稱", placeholder=_default_name(seat), key=_name_key(seat)
    )
    character_column.selectbox(
        f"玩家 {seat} 角色",
        list(catalog.CHARACTERS_BY_KEY),
        index=seat - 1,
        format_func=lambda key: catalog.CHARACTERS_BY_KEY[key].label,
        key=_character_key(seat),
    )


def _start_game() -> str:
    player_count = st.session_state[_PLAYER_COUNT_KEY]
    session.start_game(Game.start([_seat_entry(seat) for seat in range(1, player_count + 1)]))
    return "遊戲開始！"


def _seat_entry(seat: int) -> tuple[str, Character]:
    name = st.session_state[_name_key(seat)].strip() or _default_name(seat)
    return name, catalog.CHARACTERS_BY_KEY[st.session_state[_character_key(seat)]]


def _default_name(seat: int) -> str:
    return f"玩家 {seat}"


def _name_key(seat: int) -> str:
    return f"setup-name-{seat}"


def _character_key(seat: int) -> str:
    return f"setup-character-{seat}"


def _render_character_reference() -> None:
    st.dataframe(
        [
            {
                "角色": character.label,
                "每回合支出": character.base_upkeep,
                "系統自動套用": describe_character(character),
            }
            for character in catalog.CHARACTERS
        ],
        hide_index=True,
        width="stretch",
        column_config={"每回合支出": MONEY_COLUMN},
    )
