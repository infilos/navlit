import time
import streamlit as st

from loguru import logger
from streamlit_extras.row import row
from utils import not_empty
from models.user import hash_password, User, validate_email, validate_password, AdminEmail, Operator, Admin
from layout import set_tab_fontsize


def show_account():
    if st.session_state.get("user") is not None:
        show_logout_form()
        # Admin user audit
        if AdminEmail == st.session_state.user.email:
            build_audit_user_list()
    elif st.session_state.get("registered") is not None:
        st.session_state.registered = None
        show_login_dialog()
    else:
        _, col2, _ = st.columns([0.25, 0.5, 0.25], gap='small')
        with col2:
            login_button = st.button("Login", type='primary', use_container_width=True)
            register_button = st.button("Register", type='secondary', use_container_width=True)
            if login_button:
                show_login_dialog()
            if register_button:
                show_register_dialog()


def show_logout_form():
    _, col2, _ = st.columns([0.25, 0.5, 0.25], gap='small')

    with col2:
        st.write(f"Already login as {st.session_state.user.name}")
        submit_button = st.button("Logout", type='primary', use_container_width=True)

        if submit_button:
            st.session_state.user = None
            st.write("You are logout. Redirecting...")
            time.sleep(1)
            st.rerun()


@st.experimental_dialog("Login")
def show_login_dialog():
    with st.form("Login"):
        email = st.text_input("Email")
        senha = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign in", type='primary')

        if submit_button:
            senha_hash = hash_password(senha)
            if user := User.check_user_login(email, senha_hash):
                st.session_state.user = user
                st.success('Login successful! Redirecting...')
                time.sleep(1)
                st.rerun()
            else:
                st.error("Login failed.")


@st.experimental_dialog("Register")
def show_register_dialog():
    with st.form("Register"):
        email = st.text_input("Email")
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        c_password = st.text_input("Confirm password", type="password")
        submit_button = st.form_submit_button("Create account", type='primary')

        if submit_button:
            if not validate_email(email):
                st.error("Invalid email.")
            elif not validate_password(password):
                st.error("The password must be at least 8 characters long.")
            elif password != c_password:
                st.error("Passwords do not match.")
            elif User.user_exists(email):
                st.error("User already exists!")
            else:
                name = name if not_empty(name) else email.split("@")[0]
                user = User.create_user(email, name, hash_password(password), role=Operator, actived=False)
                st.success("User created successfully!")
                with st.spinner('Redirecting you to the login screen...'):
                    time.sleep(2)
                    st.session_state.registered = True
                    st.rerun()


@st.experimental_dialog("Delete User")
def show_delete_user_dialog(user: User):
    st.text(f"Name: {user.name}")
    st.text(f"Email: {user.email}")
    st.text(f"Role: {user.role}")
    if st.button("Are you sure?"):
        try:
            User.delete_user(user.email)
            st.info("Delete success!")
            st.rerun()
        except Exception as e:
            st.error(f"Delete user failed: {e}")


@st.experimental_dialog("Update User")
def show_update_user_dialog(user: User):
    all_roles = [Admin, Operator]
    select_index = all_roles.index(user.role)

    st.text_input("Email", value=user.email, disabled=True)
    name = st.text_input("Name", value=user.name)
    role = st.selectbox("Role", options=all_roles, index=select_index, placeholder="Select Role...")

    if st.button("Submit"):
        if name and role:
            try:
                User.update_user(
                    email=user.email,
                    name=name,
                    role=role,
                )
                st.rerun()
            except Exception as e:
                st.error(f"Update user failed: {e}")
        else:
            st.error("Name, Role fields are required!")


def build_audit_user_list():
    set_tab_fontsize(20)
    with st.tabs(["User Manage"])[0]:
        all_users = User.find_all()
        row_spec = [1, 2, 4, 2, 2, 2, 2]
        field_names = ["ID", "Name", "Email", "Role", "Actived", "Delete", "Update"]
        field_row = row(row_spec, vertical_align="center")
        for field in field_names:
            field_row.write(field)

        for user in all_users:
            each_row = st.columns(row_spec)
            each_row[0].write(user.id)
            each_row[1].write(user.name)
            each_row[2].write(user.email)
            each_row[3].write(user.role)

            if user.actived:
                if each_row[4].button("Deactive", key=f"user_{user.id}_deactive", use_container_width=True):
                    User.update_user(email=user.email, actived=False)
                    st.rerun()
            else:
                if each_row[4].button("Acitive", key=f"user_{user.id}_active", use_container_width=True):
                    User.update_user(email=user.email, actived=True)
                    st.rerun()
            if each_row[5].button("Delete", key=f"user_{user.id}_delete", use_container_width=True):
                show_delete_user_dialog(user)
            if each_row[6].button("Update", key=f"user_{user.id}_update", use_container_width=True):
                show_update_user_dialog(user)
