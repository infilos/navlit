import streamlit as st
from loguru import logger

from layout import set_tab_fontsize
from models.favorite import Favorite
from models.user import User, Guest
from models.website import Website
from pages.card import build_card
from pages.manage import show_create_dialog
from streamlit.runtime.scriptrunner import get_script_run_ctx

FavoriteCategory = "Favorite"


def show_navlit():
    set_tab_fontsize(20)
    user_ip = get_script_run_ctx().session_id.replace("-", "")
    logger.info(f"user session: {user_ip}")

    all_websites = list()
    all_categories = list()

    submit_col, search_col = st.columns([1, 1], gap="small")
    with search_col:
        search = st.text_input(
            "Search Keyword",
            placeholder="Type keyword to search...",
            label_visibility="collapsed"
        )
        all_websites = Website.find_all_websites(search)
        all_categories = list(set(map(lambda x: x.category, all_websites)))
    with submit_col:
        submit = st.button("Submit Website", use_container_width=True)
        if submit:
            show_create_dialog(all_categories)

    all_favorites = list()
    if st.session_state.get("user") is not None:
        logger.info(f"user_email found: {st.session_state.user.email}")
        all_favorites = Favorite.find_user_favorites(st.session_state.user.email)
    else:
        logger.info(f"user_email missing")

    print(f"all_favorites: {all_favorites}")
    all_favorite_website_ids: set[int] = set(map(lambda x: x.website_id, all_favorites))
    exists_favorite = len(all_favorite_website_ids) > 0

    categories_without_favorite = set()
    category_map_to_websites = dict()
    if exists_favorite:
        category_map_to_websites[FavoriteCategory] = list()
    for website in all_websites:
        if website.id in all_favorite_website_ids:
            category_map_to_websites[FavoriteCategory].append(website)
        elif website.category in category_map_to_websites:
            categories_without_favorite.add(website.category)
            category_map_to_websites[website.category].append(website)
        else:
            categories_without_favorite.add(website.category)
            category_map_to_websites[website.category] = [website]

    if exists_favorite:
        all_categories = [FavoriteCategory]
        all_categories.extend(categories_without_favorite)
        all_categories.sort()
        tabs = st.tabs(all_categories)
    else:
        all_categories = list(categories_without_favorite)
        all_categories.sort()
        tabs = st.tabs(all_categories)

    user_email_to_name = User.find_user_email_to_name_map()

    for tab, tab_name in zip(tabs, all_categories):
        with tab:
            is_favorite = FavoriteCategory == tab_name
            col1, col2, col3 = st.columns(3, gap="small")

            category_websites = category_map_to_websites.get(tab_name)
            logger.info("tab_name: " + str(tab_name))
            logger.info("category_websites: " + str(category_websites))
            all_rows = [category_websites[i:i + 3] for i in range(0, len(category_websites), 3)]
            for each_row in all_rows:
                with col1:
                    website = each_row[0]
                    build_card(website, is_favorite, user_email_to_name[website.owner], user_ip=user_ip)
                if len(each_row) < 2:
                    continue
                with col2:
                    website = each_row[1]
                    build_card(website, is_favorite, user_email_to_name[website.owner], user_ip=user_ip)
                if len(each_row) < 3:
                    continue
                with col3:
                    website = each_row[2]
                    build_card(website, is_favorite, user_email_to_name[website.owner], user_ip=user_ip)
