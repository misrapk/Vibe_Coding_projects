import streamlit as st
from src.frontend.api_client import login, register, get_me

def show_login():
    st.subheader("Welcome Back")
    st.write("Login to access your dashboard")
    
    with st.container():
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In"):
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                with st.spinner("Authenticating..."):
                    result, error = login(email, password)
                    if error:
                        st.error(f"Login failed: {error}")
                    else:
                        st.session_state.token = result["access_token"]
                        # Fetch user details
                        user_data, user_error = get_me()
                        if user_error:
                            st.error(f"Could not fetch user profile: {user_error}")
                        else:
                            st.session_state.user = user_data
                            st.session_state.authenticated = True
                            st.success("Login successful!")
                            st.rerun()

def show_register():
    st.subheader("Create Account")
    st.write("Join the AI-powered recruitment platform")
    
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
        email = st.text_input("Email Address")
    with col2:
        last_name = st.text_input("Last Name")
        password = st.text_input("Password", type="password")
    
    confirm_password = st.text_input("Confirm Password", type="password")
    role = st.radio("I am a:", ["candidate", "recruiter"], horizontal=True)
    
    if st.button("Register"):
        if not all([first_name, last_name, email, password]):
            st.error("All fields are required")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif len(password) < 8:
            st.error("Password must be at least 8 characters")
        else:
            with st.spinner("Creating account..."):
                result, error = register(email, password, first_name, last_name, role)
                if error:
                    st.error(f"Registration failed: {error}")
                else:
                    st.success("Account created successfully! Please log in.")
                    # Optionally switch to login page automatically
                    # st.session_state.auth_mode = "Login" 
                    # st.rerun()
