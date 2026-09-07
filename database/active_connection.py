import streamlit as st

from database.connection import engine as default_engine


def get_active_engine():
    """
    Return the currently selected database engine.

    If an external database is connected, use that engine.
    Otherwise, use the original application database engine.
    """

    active_engine = st.session_state.get(
        "active_engine"
    )

    if active_engine is not None:
        return active_engine

    return default_engine