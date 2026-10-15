"""Streamlit entry point for the Industry Tycoon companion app.

Run with::

    streamlit run app.py
"""

import streamlit as st

from industry_tycoon.ui import game_view, session, setup_view


def main() -> None:
    st.set_page_config(page_title="Industry Tycoon", page_icon="🏭", layout="wide")
    session.show_notifications()

    game = session.get_game()
    if game is None:
        setup_view.render()
    else:
        game_view.render(game)


if __name__ == "__main__":
    main()
