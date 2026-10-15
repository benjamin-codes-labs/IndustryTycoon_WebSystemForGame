"""Exceptions raised by the game engine."""


class GameRuleError(Exception):
    """An action was rejected because it would break a game rule.

    The message is written for players and is shown verbatim in the UI.
    """
