"""Typed access to Streamlit session state, plus toast notifications for actions."""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from industry_tycoon.errors import GameRuleError
from industry_tycoon.game import Game

_GAME_KEY = "game"
_NOTIFICATIONS_KEY = "notifications"


def get_game() -> Game | None:
    return st.session_state.get(_GAME_KEY)


def start_game(game: Game) -> None:
    st.session_state[_GAME_KEY] = game


def end_game() -> None:
    st.session_state.pop(_GAME_KEY, None)


def notify(message: str, *, icon: str = "✅") -> None:
    """Queue a toast to be shown during the next script run.

    Widget callbacks run before the script body, so their outcomes are queued
    here and rendered by :func:`show_notifications`.
    """
    st.session_state.setdefault(_NOTIFICATIONS_KEY, []).append((message, icon))


def show_notifications() -> None:
    for message, icon in st.session_state.pop(_NOTIFICATIONS_KEY, []):
        st.toast(message, icon=icon)


def perform(action: Callable[..., str], *args: object) -> None:
    """Widget callback adapter: run a game action and report its outcome as a toast.

    ``action`` returns a success message or raises :class:`GameRuleError` with
    a player-facing explanation of why the action was rejected.
    """
    try:
        message = action(*args)
    except GameRuleError as error:
        notify(str(error), icon="⚠️")
    else:
        notify(message)


def reset_widgets(*key_prefixes: str) -> None:
    """Return widgets whose keys start with any of ``key_prefixes`` to their defaults."""
    for key in [key for key in st.session_state if str(key).startswith(key_prefixes)]:
        del st.session_state[key]
