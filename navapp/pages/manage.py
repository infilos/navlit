import io

import requests
import streamlit as st
from PIL import Image
from streamlit_extras.row import row
from st_btn_group import st_btn_group
from pages.user import show_login_dialog
from models.website import Website
from models.user import AdminEmail, GuestEmail
from pages.card import build_card
from layout import set_tab_fontsize


def load_image(url: str):
    img = Image.open(requests.get(url, stream=True).raw)
    img_arr = io.BytesIO()
    img.save(img_arr, format=img.format)
    return img_arr.getvalue()


@st.experimental_dialog("Create Website")
def show_create_dialog(all_categories: list[str]):
    categories = list()
    if "Create New Category..." not in categories:
        categories = ["Create New Category..."] + all_categories
    else:
        categories = all_categories

    select_category = st.selectbox("Category", options=categories, index=0, placeholder="Select Category...")
    need_create_category = select_category == "Create New Category..."
    if need_create_category:
        create_category = st.text_input("New Category")
    else:
        create_category = None
    actual_category = create_category if create_category else select_category

    name = st.text_input("Name")
    descr = st.text_input("Description")
    url = st.text_input("Url")
    img_url = st.text_input("Image", placeholder="Input image url...")
    img_data = None
    img_preview = st.button("Preview", use_container_width=True)
    img_preview_holder = st.empty()
    if img_preview:
        try:
            img_data = load_image(img_url)
            img_preview_holder = st.columns(3)[1].image(img_data, use_column_width=True)
        except Exception as e:
            st.error(f"Load image failed: {img_url}, {e}")
            img_preview_holder = st.columns(3)[1].image(img_url, use_column_width=True)
    img_upload = st.file_uploader("Upload", label_visibility="collapsed", accept_multiple_files=False)
    if img_upload is not None:
        img_data = img_upload.getvalue()
        img_preview_holder = st.columns(3)[1].image(img_data, use_column_width=True)

    if st.button("Submit"):
        if actual_category and name and url:
            try:
                Website.create_website(
                    category=actual_category,
                    name=name,
                    url=url,
                    creator=st.session_state.user.email if "user" in st.session_state else GuestEmail,
                    acvited=False,
                    descr=descr,
                    img_url=img_url,
                    img_data=img_data
                )
                st.rerun()
            except Exception as e:
                st.error(f"Update website failed: {e}")
        else:
            st.error("Category, Name, Url fields are required!")


@st.experimental_dialog("Delete Website")
def show_delete_dialog(_id: int, _category: str, _name: str):
    st.text(f"ID: {_id}")
    st.text(f"Category: {_category}")
    st.text(f"Name: {_name}")
    if st.button("Are you sure?"):
        try:
            Website.delete_website(_id)
            st.info("Delete success!")
            st.rerun()
        except Exception as e:
            st.error(f"Delete website failed: {e}")


@st.experimental_dialog("Update Website")
def show_update_dialog(all_categories: list[str], _id: int, _category: str, _name: str, _descr: str, _url: str, _img_url: str, _img_data: bytes, _actived: bool):
    select_index = all_categories.index(_category)
    select_category = st.selectbox("Category", options=all_categories, index=select_index, placeholder="Select Category...")
    need_create_category = select_category == "Create New Category..."
    if need_create_category:
        create_category = st.text_input("New Category")
    else:
        create_category = None
    actual_category = create_category if create_category else select_category

    name = st.text_input("Name", value=_name)
    descr = st.text_input("Descr", value=_descr)
    url = st.text_input("Url", value=_url)
    img_url = st.text_input("Image", value=_img_url)

    img_data = _img_data
    img_preview = st.button("Preview", use_container_width=True)
    img_preview_holder = st.empty()
    if img_preview and (img_data is not None or img_url is not None):
        try:
            if img_data is not None and img_url == _img_url:
                img_preview_holder = st.columns(3)[1].image(img_data, use_column_width=True)
            else:
                img_data = load_image(img_url)
                img_preview_holder = st.columns(3)[1].image(img_data, use_column_width=True)
        except Exception as e:
            st.error(f"Load image failed: {img_url}, {e}")
            img_preview_holder = st.columns(3)[1].image(img_url, use_column_width=True)
    img_upload = st.file_uploader("Upload", label_visibility="collapsed", accept_multiple_files=False)
    if img_upload is not None:
        img_data = img_upload.getvalue()
        img_preview_holder = st.columns(3)[1].image(img_data, use_column_width=True)

    if st.button("Submit"):
        if (select_category or create_category) and name and url:
            try:
                Website.update_website(
                    _id=_id,
                    updater=st.session_state.user.email,
                    category=actual_category,
                    name=name,
                    descr=descr,
                    url=url,
                    img_url=img_url,
                    img_data=img_data,
                )
                st.rerun()
            except Exception as e:
                st.error(f"Update website failed: {e}")
        else:
            st.error("Category, Name, Url fields are required!")


@st.experimental_dialog("Website Detail")
def show_detail_dialog(_id: int, _category: str, _name: str, _descr: str, _url: str, _img_url: str, _img_data: bytes, _actived: bool):
    catetory = st.text_input("Category", value=_category, disabled=True)
    name = st.text_input("Name", value=_name, disabled=True)
    descr = st.text_input("Descr", value=_descr, disabled=True)
    url = st.text_input("Url", value=_url, disabled=True)
    img_url = st.text_input("Image", value=_img_url, disabled=True)
    img_data = _img_data
    img_preview_holder = st.empty()
    if img_data is not None:
        try:
            img_preview_holder = st.columns(3)[1].image(img_data, use_column_width=True)
        except Exception as e:
            st.error(f"Load image failed: {img_url}, {e}")
            img_preview_holder = st.columns(3)[1].image(img_url, use_column_width=True)


# issue: cannot refresh the icon, rerun will keep loop
def build_active_btn(_id: int, actived: bool):
    website_active_state_key = f"website_active_state_{_id}"
    if website_active_state_key not in st.session_state:
        st.session_state[website_active_state_key] = actived

    current_actived = st.session_state[website_active_state_key]
    active_icon = "<i class='fa-solid fa-heart'></i>" if current_actived else "<i class='fa-regular fa-heart'></i>"
    buttons = [{
        "label": active_icon,
        "value": "active",
    }]
    clicked = st_btn_group(buttons=buttons, key=f"active_{_id}", shape='square', size='compact', align='right', disabled=False, merge_buttons=False, gap_between_buttons=0, display_divider=True, return_value=True)
    if clicked:
        st.session_state[website_active_state_key] = not current_actived
        Website.update_website(_id, st.session_state.user.email, actived=not current_actived)


def build_list(all_websites: list, all_categories: list, list_type: str):
    row_spec = [1, 2, 2, 4, 3, 2, 2, 2]
    field_names = ["ID", "Category", "Name", "Url", "Actived", "Delete", "Update", "Detail"]
    field_row = row(row_spec, vertical_align="center")
    for field in field_names:
        field_row.write(field)

    for website in all_websites:
        each_row = st.columns(row_spec)
        each_row[0].write(website.id)
        each_row[1].write(website.category)
        each_row[2].write(website.name)
        each_row[3].write(website.url)

        if website.actived:
            if each_row[4].button("Deactive", key=f"{list_type}_{website.id}_deactive"):
                Website.update_website(website.id, st.session_state.user.email, actived=False)
                st.rerun()
        else:
            if each_row[4].button("Acitive", key=f"{list_type}_{website.id}_active"):
                Website.update_website(website.id, st.session_state.user.email, actived=True)
                st.rerun()
        if each_row[5].button("Delete", key=f"{list_type}_{website.id}_delete"):
            show_delete_dialog(website.id, website.category, website.name)
        if each_row[6].button("Update", key=f"{list_type}_{website.id}_update"):
            show_update_dialog(all_categories, website.id, website.category, website.name, website.descr, website.url, website.img_url, website.img_data, website.actived)
        # dialog still exists bug
        # if each_row[7].button("Detail", key=f"{website.id}_detail"):
        #     show_detail_dialog(website.id, website.category, website.name, website.descr, website.url, website.img_url, website.img_data, website.actived)
        with each_row[7].popover("View"):
            build_card(website, False, website.owner.split("@")[0], "view")

        # use Row Layout, but exists issue
        # each_row = row([1, 2, 2, 2, 4, 4, 2, 2, 2], vertical_align="center")
        # each_row.write(website.id)
        # each_row.write(website.category)
        # each_row.write(website.name)
        # each_row.write(website.descr if website.descr else "")
        # each_row.write(website.url)
        # each_row.write(website.img_url if website.img_url else "")
        # # if website.actived:
        # #     if each_row.button("Deactive", key=f"{website.id}_deactive"):
        # #         Website.update_website(website.id, st.session_state.user.email, actived=False)
        # #         st.rerun()
        # # else:
        # #     if each_row.button("Acitive", key=f"{website.id}_active"):
        # #         Website.update_website(website.id, st.session_state.user.email, actived=True)
        # #         st.rerun()
        #
        # toggle_state_key = f"toggle_active_{website.id}"
        # if toggle_state_key not in st.session_state:
        #     st.session_state[toggle_state_key] = website.actived
        # if each_row.toggle(f"active_{website.id}", value=st.session_state[toggle_state_key], label_visibility="collapsed", key=toggle_state_key):
        #     Website.update_website(website.id, st.session_state.user.email, actived=not website.actived)
        #
        # if each_row.button("Delete", key=f"{website.id}_delete"):
        #     show_delete_dialog(website.id, website.category, website.name)
        # if each_row.button("Update", key=f"{website.id}_update"):
        #     show_update_dialog(all_categories, website.id, website.category, website.name, website.url, website.img_url, website.actived)


def show_manage():
    set_tab_fontsize(20)

    if st.session_state.get("user") is None:
        show_login_dialog()
    else:
        st.write(f"Already login as {st.session_state.user.name}")

        user_email = st.session_state.user.email
        is_admin_user = AdminEmail == user_email

        all_websites = list()
        all_categories = list()

        submit_col, search_col = st.columns([1, 1], gap="small")
        with search_col:
            search = st.text_input(
                "Search Keyword",
                placeholder="Type keyword to search...",
                label_visibility="collapsed"
            )
            all_websites = Website.find_all_websites(search) if is_admin_user else Website.find_all_websites(search, creator=user_email)
            all_categories = list(set(map(lambda x: x.category, all_websites)))
        with submit_col:
            create_button = st.button("Create Website", use_container_width=True)
            if create_button:
                show_create_dialog(all_categories)

        if not is_admin_user:
            build_list(all_websites, all_categories, "manage")
        else:
            all_websites_tab, waiting_audit_tab = st.tabs(["All Websites", "Waiting Audit"])
            with all_websites_tab:
                build_list(all_websites, all_categories, "manage")
            with waiting_audit_tab:
                all_websites = Website.find_all_websites(creator=GuestEmail, actived=False)
                build_list(all_websites, all_categories, "audit")
