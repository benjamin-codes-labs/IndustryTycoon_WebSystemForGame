"""Static game content: raw resources, processed goods, pieces and characters.

These tables are the single source of truth for the game's balance. Prices
here are *base* prices; live, inflation-adjusted prices are tracked by
:class:`industry_tycoon.market.Market`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RawResource:
    """A resource gathered from the map, either from cards or by collection plants."""

    key: str
    label: str
    price: int
    plant_cost: int
    #: Units each collection plant yields at the start of its owner's turn.
    output_per_plant: int
    #: Weight of one unit when measuring the price level for inflation.
    inflation_weight: int


@dataclass(frozen=True)
class ProcessedGood:
    """A good produced by investing raw resources into a processing plant."""

    key: str
    label: str
    plant_label: str
    price: int
    plant_cost: int
    inputs: tuple[str, ...]
    #: Value of the output relative to the market value of the invested inputs.
    value_multiplier: int


@dataclass(frozen=True)
class Piece:
    """A playing piece. Pieces without a price are obtained by synthesis or card effects."""

    key: str
    label: str
    price: int | None = None
    #: Pieces this one is synthesized from; its value is the sum of theirs.
    components: tuple[str, ...] = ()

    @property
    def is_purchasable(self) -> bool:
        return self.price is not None


@dataclass(frozen=True)
class Character:
    """A playable character and the modifiers the app applies on their behalf."""

    key: str
    label: str
    base_upkeep: int
    sale_multiplier: float = 1.0
    build_cost_multiplier: float = 1.0
    piece_cost_multiplier: float = 1.0
    collection_output_multiplier: float = 1.0
    processed_output_multiplier: float = 1.0
    #: Money earned for each enemy piece captured.
    capture_bounty: int = 0


Resource = RawResource | ProcessedGood


# fmt: off
RAW_RESOURCES: tuple[RawResource, ...] = (
    #           key          label     price plant_cost output_per_plant inflation_weight
    RawResource("wood",      "木材",   60,   670,       3,               25),
    RawResource("iron_ore",  "鐵",     160,  1200,      2,               50),
    RawResource("gold",      "黃金",   600,  2400,      1,               250),
    RawResource("crude_oil", "原油",   400,  1680,      1,               200),
    RawResource("fish",      "魚",     48,   480,       3,               20),
    RawResource("crop",      "農作物", 40,   480,       3,               20),
    RawResource("meat",      "肉",     46,   530,       2,               20),
    RawResource("stone",     "石頭",   80,   864,       3,               25),
    RawResource("coal",      "煤炭",   120,  1250,      3,               100),
    RawResource("livestock", "畜牧",   44,   510,       3,               25),
)
# fmt: on

PROCESSED_GOODS: tuple[ProcessedGood, ...] = (
    ProcessedGood(
        "steel",
        "鋼鐵",
        plant_label="鋼鐵加工廠",
        price=840,
        plant_cost=2510,
        inputs=("fine_iron", "coal"),
        value_multiplier=3,
    ),
    ProcessedGood(
        "fine_iron",
        "精鐵",
        plant_label="精鐵加工廠",
        price=320,
        plant_cost=950,
        inputs=("iron_ore",),
        value_multiplier=2,
    ),
    ProcessedGood(
        "gasoline",
        "汽油",
        plant_label="煉油加工廠",
        price=800,
        plant_cost=2300,
        inputs=("crude_oil",),
        value_multiplier=2,
    ),
    ProcessedGood(
        "food",
        "食物",
        plant_label="食物加工廠",
        price=270,
        plant_cost=600,
        inputs=("fish", "crop", "meat"),
        value_multiplier=2,
    ),
    ProcessedGood(
        "building_material",
        "建材",
        plant_label="建材加工廠",
        price=600,
        plant_cost=1500,
        inputs=("wood", "stone", "fine_iron"),
        value_multiplier=2,
    ),
)

PIECES: tuple[Piece, ...] = (
    Piece("king", "國王"),
    Piece("queen", "皇后", components=("bishop", "castle")),
    Piece("general", "將軍", components=("castle", "knight")),
    Piece("castle", "城堡", price=660),
    Piece("bishop", "主教", price=400),
    Piece("knight", "騎士", price=400),
    Piece("soldier", "士兵", price=130),
)

CHARACTERS: tuple[Character, ...] = (
    Character(
        "edison", "愛迪生", base_upkeep=225, sale_multiplier=2, processed_output_multiplier=1.75
    ),
    Character("tesla", "特斯拉", base_upkeep=100),
    Character(
        "cixi",
        "慈禧",
        base_upkeep=0,
        sale_multiplier=0.7,
        build_cost_multiplier=0.9,
        collection_output_multiplier=0.7,
    ),
    Character("nicholas_ii", "尼古拉斯二世", base_upkeep=150),
    Character("yuan_longping", "袁隆平", base_upkeep=250, sale_multiplier=3),
    Character("genghis_khan", "成吉思汗", base_upkeep=150, capture_bounty=175),
    Character(
        "qin_shi_huang",
        "秦始皇",
        base_upkeep=250,
        build_cost_multiplier=0.5,
        piece_cost_multiplier=0.5,
    ),
    Character("meiji", "明治天皇", base_upkeep=225),
    Character("roosevelt", "羅斯福", base_upkeep=175, sale_multiplier=0.5),
    Character("liu_xiu", "劉秀", base_upkeep=300),
    Character("oppenheimer", "奧本海默", base_upkeep=170, capture_bounty=50),
    Character("frederick_ii", "腓特烈二世", base_upkeep=400),
)

RESOURCES: tuple[Resource, ...] = RAW_RESOURCES + PROCESSED_GOODS

RAW_RESOURCES_BY_KEY: dict[str, RawResource] = {item.key: item for item in RAW_RESOURCES}
PROCESSED_GOODS_BY_KEY: dict[str, ProcessedGood] = {item.key: item for item in PROCESSED_GOODS}
RESOURCES_BY_KEY: dict[str, Resource] = {item.key: item for item in RESOURCES}
PIECES_BY_KEY: dict[str, Piece] = {item.key: item for item in PIECES}
CHARACTERS_BY_KEY: dict[str, Character] = {item.key: item for item in CHARACTERS}
