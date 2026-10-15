"""Presentation helpers shared across views."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from typing import Protocol, TypeVar

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from industry_tycoon.catalog import Character
from industry_tycoon.formatting import CURRENCY_SYMBOL, money

T = TypeVar("T")

#: Dataframe column config for amounts of money (cells keep numeric sorting).
MONEY_COLUMN = st.column_config.NumberColumn(format=f"{CURRENCY_SYMBOL}%d")


class Labelled(Protocol):
    @property
    def label(self) -> str: ...


def grid(items: Sequence[T], columns: int) -> Iterator[tuple[DeltaGenerator, T]]:
    """Lay ``items`` out in rows of ``columns``, yielding each item with its column."""
    for start in range(0, len(items), columns):
        row = items[start : start + columns]
        yield from zip(st.columns(columns), row, strict=False)


def format_counts(counts: Mapping[str, int], catalog_by_key: Mapping[str, Labelled]) -> str:
    """Render holdings as ``"木材 ×3、魚 ×2"``, or an em dash when there are none."""
    parts = [f"{catalog_by_key[key].label} ×{count}" for key, count in counts.items() if count > 0]
    return "、".join(parts) or "—"


def describe_character(character: Character) -> str:
    """Summarise the modifiers the app applies automatically for a character."""
    modifiers = [
        ("出售收入", character.sale_multiplier),
        ("建造成本", character.build_cost_multiplier),
        ("棋子價格", character.piece_cost_multiplier),
        ("收集廠產量", character.collection_output_multiplier),
        ("加工產出", character.processed_output_multiplier),
    ]
    effects = [f"{name} ×{value:g}" for name, value in modifiers if value != 1]
    if character.capture_bounty:
        effects.append(f"擊殺獎勵 {money(character.capture_bounty)}")
    return "・".join(effects) or "無自動修正"
