"""End-to-end smoke tests that drive the real Streamlit script headlessly."""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from industry_tycoon import rules

APP_PATH = str(Path(__file__).resolve().parents[1] / "app.py")


@pytest.fixture
def app() -> AppTest:
    app = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not app.exception
    return app


def _start_game(app: AppTest) -> None:
    app.text_input(key="setup-name-1").input("Alice")
    app.text_input(key="setup-name-2").input("Bob")
    app.button(key="start-game").click().run()
    assert not app.exception


def test_setup_creates_the_game(app: AppTest):
    _start_game(app)

    game = app.session_state["game"]
    assert [player.name for player in game.players] == ["Alice", "Bob", "玩家 3", "玩家 4"]


def test_player_count_controls_the_number_of_seats(app: AppTest):
    app.radio(key="setup-player-count").set_value(2).run()
    app.button(key="start-game").click().run()

    assert len(app.session_state["game"].players) == 2


def test_setup_rejects_duplicate_names(app: AppTest):
    app.text_input(key="setup-name-1").input("Alice")
    app.text_input(key="setup-name-2").input("Alice")
    app.button(key="start-game").click().run()

    assert not app.exception
    assert "game" not in app.session_state
    assert any("重複" in toast.value for toast in app.toast)


def test_actions_and_turn_handover(app: AppTest):
    _start_game(app)

    app.button(key="take-wood").click().run()
    app.button(key="end-turn").click().run()

    assert not app.exception
    game = app.session_state["game"]
    assert game.players[0].inventory["wood"] == 1
    assert game.current_player.name == "Bob"


def test_rejected_action_is_reported_instead_of_crashing(app: AppTest):
    _start_game(app)

    app.button(key="build-collection-gold").click().run()

    assert not app.exception
    assert any("金錢不足" in toast.value for toast in app.toast)
    assert app.session_state["game"].current_player.money == rules.STARTING_MONEY
