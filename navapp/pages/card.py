import webbrowser as wb

import streamlit as st
from loguru import logger
from streamlit_extras.stylable_container import stylable_container

from models.website import Website
from models.favorite import Favorite
from models.trend import Trend


def build_card(website: Website, is_favorite: bool, owner: str = None, card_type: str = "normal", user_ip: str = None):
    with stylable_container(
            key=f"build_card_5_{website.id}_{card_type}",
            css_styles="""
            {
                height: 100%;
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                gap: 0rem;
                padding-bottom: 0.5rem;
                button[title="View fullscreen"]{visibility: hidden;}
                h2 > div > a {
                    display: none;
                }
                h3 > div > a {
                    display: none;
                }
                h4 > div > a {
                    display: none;
                }
            """
    ):
        t_col_1, t_col_2 = st.columns([10, 2], gap="small")
        t_col_1.subheader(website.name)
        if website.img_data:
            t_col_2.image(website.img_data, use_column_width=True)
        elif website.img_url:
            t_col_2.image(website.img_url, use_column_width=True)
        if website.descr:
            st.text(website.descr)
        else:
            st.markdown("#")

        if st.session_state.get("user") is not None:
            email = st.session_state.user.email
        else:
            email = None

        col_1, col_2, col_3 = st.columns([0.6, 0.2, 0.2], gap="small")
        with col_1:
            if owner:
                st.caption(f"@{owner}")
        with stylable_container(
                key=f"stylable_container_like_emoji_{website.id}_{card_type}",
                css_styles="""
            button {
                height: auto;
                width: auto;
            }
            """
        ):
            with col_2:
                if st.button(":grinning_face_with_star_eyes:", key=f"like_emoji_{website.id}_{card_type}"):
                    if email is not None:
                        if is_favorite:
                            logger.info(f"user delete favorite url: {email},{website.url}")
                            Favorite.delete_favorite(email, website.id)
                        else:
                            logger.info(f"user create favorite url: {email},{website.url}")
                            Favorite.create_favorite(email, website.id)
        with stylable_container(
                key=f"stylable_container_open_emoji_{website.id}_{card_type}",
                css_styles="""
            button {
                height: auto;
                width: auto;
            }
            """
        ):
            with col_3:
                if st.button(":rocket:", key=f"open_emoji_{website.id}_{card_type}"):
                    logger.info(f"user open url: {email},{website.url}")
                    Trend.create_trend(website.category, website.name, email, user_ip)
                    wb.open_new_tab(website.url)

        # issue: icon loading is very slow
        # col_1, col_2 = st.columns([0.6, 0.4], gap="small")
        # with col_1:
        #     if owner:
        #         st.caption(f"@{owner}")
        # with col_2:
        #     if st.session_state.get("user") is not None:
        #         email = st.session_state.user.email
        #     else:
        #         email = None
        #
        #     favorite_icon = "<i class='fa-solid fa-heart'></i>" if is_favorite else "<i class='fa-regular fa-heart'></i>"
        #     buttons = [{
        #         "label": favorite_icon,
        #         "value": "like",
        #     }, {
        #         "label": "<i class='fa-solid fa-arrow-up-right-from-square'></i>",
        #         "value": "open",
        #     }, ]
        #     clicked = st_btn_group(buttons=buttons, key=f"like_open_{_id}", shape='square', size='compact', align='right', disabled=False, merge_buttons=True, gap_between_buttons=0, display_divider=True, return_value=True)
        #     if clicked == "like":
        #         if email is not None:
        #             if is_favorite:
        #                 logger.info(f"user delete favorite url: {email},{url}")
        #                 Favorite.delete_favorite(email, _id)
        #             else:
        #                 logger.info(f"user create favorite url: {email},{url}")
        #                 Favorite.create_favorite(email, _id)
        #     elif clicked == "open":
        #         logger.info(f"user open url: {email},{url}")
        #         Trend.create_trend(category, name, email)
        #         wb.open_new_tab(url)
