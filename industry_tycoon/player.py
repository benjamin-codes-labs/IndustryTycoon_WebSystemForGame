"""Per-player state."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field

from industry_tycoon import catalog, rules
from industry_tycoon.catalog import Character
from industry_tycoon.errors import GameRuleError
from industry_tycoon.formatting import money


@dataclass
class Player:
    """Everything the app tracks for one seat at the table.

    Holdings are ``Counter`` objects keyed by catalog keys, so a missing item
    simply counts as zero.
    """

    name: str
    character: Character
    money: int = rules.STARTING_MONEY
    upkeep: int = field(init=False)
    inventory: Counter[str] = field(default_factory=Counter)
    #: Processed goods produced this turn; delivered to the inventory when the turn ends.
    pending_goods: Counter[str] = field(default_factory=Counter)
    collection_plants: Counter[str] = field(default_factory=Counter)
    processing_plants: Counter[str] = field(default_factory=Counter)
    pieces: Counter[str] = field(default_factory=Counter)
    #: Consecutive turns this player has started with no money.
    bankrupt_turns: int = 0
    eliminated: bool = False

    def __post_init__(self) -> None:
        self.upkeep = self.character.base_upkeep

    @property
    def building_count(self) -> int:
        return self.collection_plants.total() + self.processing_plants.total()

    def pay(self, amount: int) -> None:
        """Deduct ``amount``, refusing the payment if the player cannot afford it."""
        if amount > self.money:
            raise GameRuleError(f"金錢不足：需要 {money(amount)}，目前只有 {money(self.money)}")
        self.money -= amount

    def consume(self, quantities: Mapping[str, int]) -> None:
        """Remove resources from the inventory: either all of them or, if any is short, none."""
        for key, quantity in quantities.items():
            if self.inventory[key] < quantity:
                label = catalog.RESOURCES_BY_KEY[key].label
                raise GameRuleError(f"{label}不足：需要 {quantity}，目前只有 {self.inventory[key]}")
        self.inventory.subtract(quantities)
