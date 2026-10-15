"""Bookkeeping engine and Streamlit UI for the Industry Tycoon board game.

The package is split into two layers:

* The domain layer (``catalog``, ``rules``, ``player``, ``market``, ``game``)
  is plain Python with no Streamlit dependency, so it can be unit tested.
* The presentation layer (``industry_tycoon.ui``) renders the domain with
  Streamlit and translates widget callbacks into game actions.
"""
