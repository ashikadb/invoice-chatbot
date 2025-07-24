import streamlit as st

def check_login():
    st.session_state['authenticated'] = False

    with st.form("login_form"):
        st.subheader("🔐 Login to BillBanter")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            correct_user = st.secrets["credentials"]["username"]
            correct_pass = st.secrets["credentials"]["password"]

            if username == correct_user and password == correct_pass:
                st.session_state['authenticated'] = True
                st.success("Welcome aboard again! Time to decode your billing story")
            else:
                st.error("Incorrect credentials. Don't worry — we all forget sometimes!")
