import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    
    # Get admin summary
    try:
        summary_response = requests.get(f"{API_URL}/admin/summary", headers=get_headers())
        if summary_response.status_code == 200:
            summary = summary_response.json()
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Students", summary["total_students"])
            with col2:
                st.metric("Total Teachers", summary["total_teachers"])
            with col3:
                st.metric("Total Subjects", summary["total_subjects"])
            with col4:
                st.metric("Passed Students", summary["passed_students"], delta=f"{summary['passed_students']}")
            with col5:
                st.metric("Failed Students", summary["failed_students"], delta=f"-{summary['failed_students']}")
    
    except Exception as e:
        st.error(f"Error loading summary: {e}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Students", "Teachers", "Subjects", "Assignments"])
    
    with tab1:
        st.subheader("Student Management")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display students
            try:
                students_response = requests.get(f"{API_URL}/admin/students", headers=get_headers())
                if students_response.status_code == 200:
                    students = students_response.json()
                    if students:
                        df = pd.DataFrame(students)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No students found")
            except Exception as e:
                st.error(f"Error loading students: {e}")
        
        with col2:
            # Add new student
            st.subheader("Add New Student")
            with st.form("add_student"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                roll_number = st.text_input("Roll Number")
                semester = st.number_input("Semester", min_value=1, max_value=8)
                department = st.text_input("Department")
                phone = st.text_input("Phone")
                
                if st.form_submit_button("Add Student"):
                    try:
                        student_data = {
                            "username": username,
                            "password": password,
                            "full_name": full_name,
                            "email": email,
                            "roll_number": roll_number,
                            "semester": semester,
                            "department": department,
                            "phone": phone
                        }
                        response = requests.post(f"{API_URL}/admin/students", json=student_data, headers=get_headers())
                        if response.status_code == 200:
                            st.success("Student added successfully!")
                            st.rerun()
                        else:
                            st.error("Error adding student")
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Teacher Management")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display teachers
            try:
                teachers_response = requests.get(f"{API_URL}/admin/teachers", headers=get_headers())
                if teachers_response.status_code == 200:
                    teachers = teachers_response.json()
                    if teachers:
                        df = pd.DataFrame(teachers)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No teachers found")
            except Exception as e:
                st.error(f"Error loading teachers: {e}")
        
        with col2:
            # Add new teacher
            st.subheader("Add New Teacher")
            with st.form("add_teacher"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                department = st.text_input("Department")
                phone = st.text_input("Phone")
                
                if st.form_submit_button("Add Teacher"):
                    try:
                        teacher_data = {
                            "username": username,
                            "password": password,
                            "full_name": full_name,
                            "email": email,
                            "department": department,
                            "phone": phone
                        }
                        response = requests.post(f"{API_URL}/admin/teachers", json=teacher_data, headers=get_headers())
                        if response.status_code == 200:
                            st.success("Teacher added successfully!")
                            st.rerun()
                        else:
                            st.error("Error adding teacher")
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Subject Management")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display subjects
            try:
                subjects_response = requests.get(f"{API_URL}/admin/subjects", headers=get_headers())
                if subjects_response.status_code == 200:
                    subjects = subjects_response.json()
                    if subjects:
                        df = pd.DataFrame(subjects)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No subjects found")
            except Exception as e:
                st.error(f"Error loading subjects: {e}")
        
        with col2:
            # Add new subject
            st.subheader("Add New Subject")
            with st.form("add_subject"):
                subject_code = st.text_input("Subject Code")
                subject_name = st.text_input("Subject Name")
                semester = st.number_input("Semester", min_value=1, max_value=8)
                credits = st.number_input("Credits", min_value=1, value=3)
                max_marks = st.number_input("Max Marks", min_value=1, value=100)
                passing_marks = st.number_input("Passing Marks", min_value=1, value=40)
                
                if st.form_submit_button("Add Subject"):
                    try:
                        subject_data = {
                            "subject_code": subject_code,
                            "subject_name": subject_name,
                            "semester": semester,
                            "credits": credits,
                            "max_marks": max_marks,
                            "passing_marks": passing_marks
                        }
                        response = requests.post(f"{API_URL}/admin/subjects", json=subject_data, headers=get_headers())
                        if response.status_code == 200:
                            st.success("Subject added successfully!")
                            st.rerun()
                        else:
                            st.error("Error adding subject")
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Teacher-Subject Assignments")
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                teachers_response = requests.get(f"{API_URL}/admin/teachers", headers=get_headers())
                subjects_response = requests.get(f"{API_URL}/admin/subjects", headers=get_headers())
                
                if teachers_response.status_code == 200 and subjects_response.status_code == 200:
                    teachers = teachers_response.json()
                    subjects = subjects_response.json()
                    
                    teacher_options = {f"{t['full_name']} ({t['username']})": t['teacher_id'] for t in teachers}
                    subject_options = {f"{s['subject_code']} - {s['subject_name']}": s['subject_id'] for s in subjects}
                    
                    selected_teacher = st.selectbox("Select Teacher", list(teacher_options.keys()))
                    selected_subject = st.selectbox("Select Subject", list(subject_options.keys()))
                    
                    if st.button("Assign Teacher to Subject"):
                        try:
                            teacher_id = teacher_options[selected_teacher]
                            subject_id = subject_options[selected_subject]
                            
                            response = requests.post(
                                f"{API_URL}/admin/assign-teacher?teacher_id={teacher_id}&subject_id={subject_id}",
                                headers=get_headers()
                            )
                            if response.status_code == 200:
                                st.success("Assignment successful!")
                            else:
                                st.error("Error in assignment")
                        except Exception as e:
                            st.error(f"Error: {e}")
                            
            except Exception as e:
                st.error(f"Error loading data: {e}")
