import importlib
import sys

import streamlit as st


def _reload_app():
    # Reload the module so session_state toggles are set on import
    if "streamlit_app" in sys.modules:
        importlib.reload(sys.modules["streamlit_app"])
    else:
        import streamlit_app  # noqa: F401
    return importlib.import_module("streamlit_app")


def test_title_flag():
    st.session_state.clear()
    app = _reload_app()
    assert st.session_state.get("title_rendered") is True
    assert app  # appease linters


def test_sidebar_flag():
    st.session_state.clear()
    _reload_app()
    assert st.session_state.get("sidebar_initialized") is True
