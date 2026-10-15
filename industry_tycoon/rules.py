"""Scalar rule constants.

Values that belong to a specific resource, piece or character live in
:mod:`industry_tycoon.catalog` instead.
"""

MIN_PLAYERS = 2
MAX_PLAYERS = 4

STARTING_MONEY = 1_500
INSURANCE_COST = 500

#: Added to a player's per-turn upkeep every time they buy a piece.
UPKEEP_PER_PIECE_BOUGHT = 10

MAX_BUILDINGS_PER_PLAYER = 15
MAX_BUILDINGS_ON_BOARD = 28

#: A player who starts this many consecutive turns with no money is eliminated.
BANKRUPTCY_TURN_LIMIT = 3

# --- Inflation model (documented in docs/RULES.md) ---------------------------

#: Weight of one building and one piece when measuring the price level.
BUILDING_ASSET_WEIGHT = 50
PIECE_ASSET_WEIGHT = 100

#: How strongly a change in the price level moves prices at the start of a round.
INFLATION_SENSITIVITY = 0.2

#: With no history yet, the previous price level is assumed to be this share of the current one.
INITIAL_PRICE_LEVEL_RATIO = 0.95
