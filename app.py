import streamlit as st
from chatbot_page import show_chatbot_page
from data_page import show_data_page
from utils import load_users, save_user

st.set_page_config(page_title="BillBanter Login", layout="wide")

def login_ui():
    st.title("🔐 Login to BillBanter")

    login_tab, signup_tab = st.tabs(["Login", "Create Account"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success(f"🎉 Welcome back, {username}!")
            else:
                st.error("🚫 Invalid credentials. Try again!")

    with signup_tab:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if save_user(new_user.strip(), new_pass.strip()):
                st.success("✅ Account created! Please login now.")
            else:
                st.warning("😬 Username already taken! Try something else.")

# Session control
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_ui()
else:
    page = st.sidebar.selectbox("Choose Page", ["Chatbot", "Extracted Data"])

    if page == "Chatbot":
        show_chatbot_page()
    elif page == "Extracted Data":
        show_data_page()
