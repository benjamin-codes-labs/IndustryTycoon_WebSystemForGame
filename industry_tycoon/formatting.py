"""Display formatting shared by the engine's messages and the UI."""

#: Full-width dollar sign. Streamlit renders all player-facing text as Markdown, where
#: text between two ASCII "$" signs becomes LaTeX; the full-width sign is never parsed.
CURRENCY_SYMBOL = "＄"


def money(amount: float) -> str:
    """Format an amount of in-game money, e.g. ``money(1500) == "＄1,500"``."""
    return f"{CURRENCY_SYMBOL}{amount:,.0f}"
