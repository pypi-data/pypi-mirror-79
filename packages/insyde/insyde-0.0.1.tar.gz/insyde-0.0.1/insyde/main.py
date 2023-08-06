import subprocess

import streamlit as st
import pandas as pd

from tools.analyze.vulture_page import VulturePage
from tools.analyze.cohesion_page import CohesionPage
from tools.analyze.radon_cc_page import RadonCCPage
from tools.analyze.radon_raw_page import RadonRawPage

from tools.visualize.pydeps_page import PydepsPage

from tools.page import Page


pages = {
    "analyze": {
        "vulture": VulturePage,
        "cohesion": CohesionPage,
        "radon_cc": RadonCCPage,
        "radon_raw": RadonRawPage
    },
    "visualize": {
        "pydeps": PydepsPage
    }
}


# TODO: pass this folder to all tools...
# common_folder = st.sidebar.text_input("Common folder to analyze", "test_code/fixme/")

tool_type = st.sidebar.radio("Tool types", ("analyze", "visualize"))


page_name = st.sidebar.selectbox(
    "Choose:",
    list(pages[tool_type].keys()),
    index=0
)

page: Page = pages[tool_type][page_name]()

st.sidebar.markdown(page.tooltip)

page.main()





