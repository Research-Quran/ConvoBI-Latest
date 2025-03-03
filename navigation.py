import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
import Configs


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.logo("apexon logo.png",icon_image="apexon logo.png")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/app.py", label="Convo BI")
            st.page_link("pages/Import.py", label="Import Metadata")
            st.page_link("pages/ManageDB.py", label="Manage Database")
            st.page_link("pages/Summary.py", label="Database Summary")
            # st.page_link("pages/test.py", label="test")
            st.page_link(Configs.Graph_URL, label="Graph Database")
            
          

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "main":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("main.py")
    

def logout():
    st.session_state.clear()
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    st.switch_page("main.py")