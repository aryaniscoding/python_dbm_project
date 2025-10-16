import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def student_dashboard():
    st.title("🎓 Student Dashboard")
    st.write(f"Welcome, {st.session_state.full_name}")
    
    # Get student results
    try:
        results_response = requests.get(f"{API_URL}/student/results", headers=get_headers())
        if results_response.status_code == 200:
            results = results_response.json()
            
            student_info = results["student"]
            marks_data = results["marks"]
            cgpa = results["cgpa"]
            total_credits = results["total_credits"]
            passed = results["passed"]
            
            # Display student info
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Student Information")
                st.write(f"**Name:** {student_info['full_name']}")
                st.write(f"**Roll Number:** {student_info['roll_number']}")
                st.write(f"**Semester:** {student_info['semester']}")
                st.write(f"**Department:** {student_info['department']}")
                st.write(f"**Email:** {student_info['email']}")
            
            with col2:
                st.subheader("Academic Performance")
                
                # CGPA with color coding
                cgpa_color = "green" if cgpa >= 7.0 else "orange" if cgpa >= 6.0 else "red"
                st.markdown(f"**CGPA:** <span style='color: {cgpa_color}; font-size: 24px; font-weight: bold;'>{cgpa}</span>", unsafe_allow_html=True)
                
                st.write(f"**Total Credits:** {total_credits}")
                
                # Overall status
                status_color = "green" if passed else "red"
                status_text = "PASSED" if passed else "FAILED"
                st.markdown(f"**Status:** <span style='color: {status_color}; font-size: 18px; font-weight: bold;'>{status_text}</span>", unsafe_allow_html=True)
            
            st.divider()
            
            # Marks table
            st.subheader("Subject-wise Marks")
            
            if marks_data:
                # Create DataFrame
                df_marks = []
                for mark in marks_data:
                    grade_point = (mark["marks_obtained"] / mark["max_marks"]) * 10
                    status = "Pass" if mark["marks_obtained"] >= mark["passing_marks"] else "Fail"
                    
                    df_marks.append({
                        "Subject Code": mark["subject_code"],
                        "Subject Name": mark["subject_name"],
                        "Marks Obtained": mark["marks_obtained"],
                        "Max Marks": mark["max_marks"],
                        "Passing Marks": mark["passing_marks"],
                        "Credits": mark["credits"],
                        "Grade Point": round(grade_point, 2),
                        "Status": status
                    })
                
                df = pd.DataFrame(df_marks)
                
                # Color code the status column
                def color_status(val):
                    color = 'green' if val == 'Pass' else 'red'
                    return f'color: {color}; font-weight: bold'
                
                styled_df = df.style.applymap(color_status, subset=['Status'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Marks Distribution")
                    fig_bar = px.bar(
                        df, 
                        x="Subject Code", 
                        y="Marks Obtained",
                        title="Marks by Subject",
                        color="Status",
                        color_discrete_map={"Pass": "green", "Fail": "red"}
                    )
                    fig_bar.add_hline(y=df["Passing Marks"].iloc[0], line_dash="dash", line_color="orange", annotation_text="Passing Line")
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                with col2:
                    st.subheader("Performance Overview")
                    
                    # Pass/Fail pie chart
                    pass_fail_counts = df["Status"].value_counts()
                    fig_pie = px.pie(
                        values=pass_fail_counts.values,
                        names=pass_fail_counts.index,
                        title="Pass/Fail Distribution",
                        color_discrete_map={"Pass": "green", "Fail": "red"}
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Grade distribution
                st.subheader("Grade Point Analysis")
                
                # Add grade categories
                def get_grade_category(grade_point):
                    if grade_point >= 9.0:
                        return "Excellent (A+)"
                    elif grade_point >= 8.0:
                        return "Very Good (A)"
                    elif grade_point >= 7.0:
                        return "Good (B+)"
                    elif grade_point >= 6.0:
                        return "Satisfactory (B)"
                    elif grade_point >= 5.0:
                        return "Acceptable (C)"
                    else:
                        return "Needs Improvement (D/F)"
                
                df["Grade Category"] = df["Grade Point"].apply(get_grade_category)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    grade_counts = df["Grade Category"].value_counts()
                    st.bar_chart(grade_counts)
                
                with col2:
                    st.subheader("Detailed Statistics")
                    st.write(f"**Highest Marks:** {df['Marks Obtained'].max():.1f}")
                    st.write(f"**Lowest Marks:** {df['Marks Obtained'].min():.1f}")
                    st.write(f"**Average Marks:** {df['Marks Obtained'].mean():.1f}")
                    st.write(f"**Subjects Passed:** {len(df[df['Status'] == 'Pass'])}/{len(df)}")
                    
                    # Recommendations
                    st.subheader("Recommendations")
                    if cgpa >= 8.0:
                        st.success("🎉 Excellent performance! Keep up the great work!")
                    elif cgpa >= 6.5:
                        st.info("👍 Good performance! Try to improve in weaker subjects.")
                    else:
                        failed_subjects = df[df["Status"] == "Fail"]["Subject Name"].tolist()
                        if failed_subjects:
                            st.warning(f"⚠️ Need to improve in: {', '.join(failed_subjects)}")
                        st.warning("📚 Focus on studies and seek help from teachers.")
            
        else:
            st.info("No results available yet.")
            
    except Exception as e:
        st.error(f"Error loading results: {e}")
