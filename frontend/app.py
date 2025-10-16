import streamlit as st
import requests
from admin_dashboard import admin_dashboard

from teacher_dashboard import teacher_dashboard

from student_dashboard import student_dashboard

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

API_URL = "http://localhost:8000"

def login(username, password, user_type):
    try:
        response = requests.post(
            f"{API_URL}/login?user_type={user_type}",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        st.error("Unable to connect to server")
        return None

def main():
    if 'token' not in st.session_state:
        st.title("🎓 Student Management System")
        
        col1, col2, col3 = st.columns([1,2,1])
        
        with col2:
            st.subheader("Login")
            
            user_type = st.selectbox(
                "Select User Type",
                ["admin", "teacher", "student"],
                format_func=lambda x: x.title()
            )
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                if username and password:
                    token_data = login(username, password, user_type)
                    if token_data:
                        st.session_state.token = token_data["access_token"]
                        st.session_state.user_type = token_data["user_type"]
                        st.session_state.user_id = token_data["user_id"]
                        st.session_state.full_name = token_data["full_name"]
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.error("Please enter username and password")
            
            st.markdown("---")
            st.markdown("**Default Credentials:**")
            st.markdown("- Admin: `admin` / `secret`")
            st.markdown("- Teacher: `teacher1` / `secret`")  
            st.markdown("- Student: `student1` / `secret`")
    
    else:
        # Show logout button in sidebar
        with st.sidebar:
            st.write(f"Welcome, {st.session_state.full_name}")
            st.write(f"Role: {st.session_state.user_type.title()}")
            
            if st.button("Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Route to appropriate dashboard
        if st.session_state.user_type == "admin":
            admin_dashboard()
        elif st.session_state.user_type == "teacher":
            teacher_dashboard()
        elif st.session_state.user_type == "student":
            student_dashboard()

if __name__ == "__main__":
    main()
