import streamlit as st

BACKGROUND_COLOR = 'white'
COLOR = 'black'


def set_page_config():
    st.set_page_config(
        page_title="Navlit",
        layout="wide",
        initial_sidebar_state="collapsed"
    )


def set_page_menu_hide():
    hide_default_format = """
       <style>
           #MainMenu { visibility: hidden; }
           .stDeployButton { display:none; visibility: hidden; }
           footer { visibility: hidden; }
           #stDecoration { display:none; }
           [data-testid="collapsedControl"] { display: none; }
           [data-testid="stStatusWidget"] { visibility: hidden; }
       </style>
       """
    st.markdown(hide_default_format, unsafe_allow_html=True)


def set_page_container_style2(
        max_width: int = 1100,
        max_width_100_percent: bool = False,
        margin_top: int = 0,
        padding_right: int = 10,
        padding_left: int = 1,
        padding_bottom: int = 10,
        color: str = COLOR,
        background_color: str = BACKGROUND_COLOR):
    if max_width_100_percent:
        max_width_str = f'max-width: 100%;'
    else:
        max_width_str = f'max-width: {max_width}px;'
    st.markdown(
        f'''
            <style>
                div[class^='block-container'] {{ 
                    margin-top: {margin_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
            </style>
            ''',
        unsafe_allow_html=True,
    )


def set_page_container_style(
        max_width: int = 1100,
        max_width_100_percent: bool = False,
        padding_top: int = 1,
        padding_right: int = 10,
        padding_left: int = 1,
        padding_bottom: int = 10,
        color: str = COLOR,
        background_color: str = BACKGROUND_COLOR):
    if max_width_100_percent:
        max_width_str = f'max-width: 100%;'
    else:
        max_width_str = f'max-width: {max_width}px;'
    st.markdown(
        f'''
            <style>
                div[class^='block-container'] {{ 
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
            </style>
            ''',
        unsafe_allow_html=True,
    )


def set_tab_fontsize(fontsize: int = 24):
    font_css = f"""
        <style>
            button[data-baseweb="tab"] {{
                margin: 0;
                width: 100%;
            }}
            button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {{
                font-size: {fontsize}px;
                margin: 0;
                width: 100%;
            }}
        </style>
    """
    st.write(font_css, unsafe_allow_html=True)
