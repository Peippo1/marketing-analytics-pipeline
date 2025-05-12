import streamlit as st
import pytest

def test_title():
    # Test if the Streamlit app is running and rendering the title
    st.write("Testing Streamlit App")
    assert "Testing Streamlit App" in st.session_state

def test_sidebar():
    # Check if the sidebar element exists (assuming there is a sidebar)
    st.sidebar.write("Sidebar Test")
    assert "Sidebar Test" in st.session_state
