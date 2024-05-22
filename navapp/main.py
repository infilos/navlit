import argparse
import os

from loguru import logger
from streamlit_navigation_bar import st_navbar

import pages as pg
from layout import set_page_config, set_page_container_style2, set_page_menu_hide
from utils import setup_logging

# parse env argument
parser = argparse.ArgumentParser()
parser.add_argument('--env', nargs='?', const='dev', type=str, help="Startup with env: dev or pro")
args = parser.parse_args()
env = args.env

# setup style
set_page_config()
set_page_menu_hide()
set_page_container_style2(
    margin_top=-2,
    padding_right=16,
    padding_bottom=1,
    padding_left=16,
)

# setup logging
setup_logging(env, "INFO")
logger.info(f"Starting with env '{env}'.")

# setup navbar
nav_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cubes.svg")
nav_styles = {
    "nav": {
        "background-color": "var(--primary-color)",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "ul": {
        "justify-content": "flex-start",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "color": "var(--text-color)",
        "background-color": "white",
        "font-weight": "normal",
        "padding": "14px",
    }
}
nav_options = {
    "show_menu": False,
    "show_sidebar": False,
}

selected_page = st_navbar(
    pages=["Navlit", "Trends", "Manage", "Account"],
    selected="Navlit",
    logo_path=nav_logo_path,
    logo_page="Navlit",
    styles=nav_styles,
    options=nav_options,
)

nav_functions = {
    "Navlit": pg.show_navlit,
    "Trends": pg.show_trends,
    "Manage": pg.show_manage,
    "Account": pg.show_account,
}
go_to = nav_functions.get(selected_page)
if go_to:
    go_to()
