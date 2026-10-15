from __future__ import annotations

import random
from collections.abc import Callable

import pytest

from industry_tycoon import catalog
from industry_tycoon.game import Game

GameFactory = Callable[..., Game]


@pytest.fixture
def make_game() -> GameFactory:
    """Build a game whose players use the given character keys, in turn order."""

    def factory(*character_keys: str, seed: int = 0) -> Game:
        roster = [
            (f"P{seat}", catalog.CHARACTERS_BY_KEY[key])
            for seat, key in enumerate(character_keys, start=1)
        ]
        return Game.start(roster, rng=random.Random(seed))

    return factory
