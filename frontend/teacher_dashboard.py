import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def teacher_dashboard():
    st.title("👨‍🏫 Teacher Dashboard")
    st.write(f"Welcome, {st.session_state.full_name}")
    
    # Get teacher's marks data
    try:
        marks_response = requests.get(f"{API_URL}/teacher/marks", headers=get_headers())
        if marks_response.status_code == 200:
            marks_data = marks_response.json()
            
            if marks_data:
                # Convert to DataFrame
                df = pd.DataFrame(marks_data)
                
                # Display current marks with inline editing
                st.subheader("Student Marks - Edit Inline")
                st.write("You can edit marks directly in the table below. Changes will be saved when you click 'Update Marks'.")
                
                # Configure column types for data editor
                column_config = {
                    "mark_id": st.column_config.NumberColumn("ID", disabled=True, width="small"),
                    "student_name": st.column_config.TextColumn("Student Name", disabled=True),
                    "subject_code": st.column_config.TextColumn("Subject", disabled=True, width="small"),
                    "subject_name": st.column_config.TextColumn("Subject Name", disabled=True),
                    "marks_obtained": st.column_config.NumberColumn(
                        "Marks",
                        min_value=0,
                        max_value=100,
                        step=0.5,
                        format="%.1f"
                    ),
                    "max_marks": st.column_config.NumberColumn("Max Marks", disabled=True, width="small"),
                    "passing_marks": st.column_config.NumberColumn("Pass Marks", disabled=True, width="small")
                }
                
                # Create editable dataframe
                edited_df = st.data_editor(
                    df,
                    column_config=column_config,
                    disabled=["mark_id", "student_id", "subject_id", "student_name", "subject_code", "subject_name", "max_marks", "passing_marks", "academic_year", "exam_type"],
                    hide_index=True,
                    use_container_width=True,
                    key="marks_editor"
                )
                
                # Update marks button
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("Update Marks", type="primary"):
                        try:
                            # Prepare marks update data
                            marks_updates = []
                            for _, row in edited_df.iterrows():
                                marks_updates.append({
                                    "mark_id": int(row["mark_id"]) if pd.notna(row["mark_id"]) else None,
                                    "student_id": int(row["student_id"]),
                                    "subject_id": int(row["subject_id"]),
                                    "marks_obtained": float(row["marks_obtained"]),
                                    "academic_year": row["academic_year"]
                                })
                            
                            # Send update request
                            response = requests.post(
                                f"{API_URL}/teacher/marks",
                                json=marks_updates,
                                headers=get_headers()
                            )
                            
                            if response.status_code == 200:
                                st.success("Marks updated successfully!")
                                st.rerun()
                            else:
                                st.error("Error updating marks")
                                
                        except Exception as e:
                            st.error(f"Error updating marks: {e}")
                
                with col2:
                    if st.button("Refresh Data"):
                        st.rerun()
                
                # Show statistics
                st.subheader("Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_students = len(edited_df["student_id"].unique())
                    st.metric("Total Students", total_students)
                
                with col2:
                    subjects = edited_df["subject_name"].unique()
                    st.metric("Subjects Teaching", len(subjects))
                
                with col3:
                    avg_marks = edited_df["marks_obtained"].mean()
                    st.metric("Average Marks", f"{avg_marks:.1f}")
                
                with col4:
                    passed_count = len(edited_df[edited_df["marks_obtained"] >= edited_df["passing_marks"]])
                    st.metric("Students Passed", passed_count)
                
                # Subject-wise breakdown
                st.subheader("Subject-wise Performance")
                
                subject_stats = edited_df.groupby(['subject_code', 'subject_name']).agg({
                    'marks_obtained': ['mean', 'min', 'max', 'count'],
                    'passing_marks': 'first'
                }).round(1)
                
                subject_stats.columns = ['Avg Marks', 'Min Marks', 'Max Marks', 'Total Students', 'Passing Marks']
                subject_stats = subject_stats.reset_index()
                
                # Calculate pass percentage
                pass_counts = []
                for _, row in subject_stats.iterrows():
                    subject_data = edited_df[edited_df['subject_code'] == row['subject_code']]
                    passed = len(subject_data[subject_data['marks_obtained'] >= subject_data['passing_marks'].iloc[0]])
                    pass_percentage = (passed / len(subject_data)) * 100
                    pass_counts.append(f"{pass_percentage:.1f}%")
                
                subject_stats['Pass %'] = pass_counts
                
                st.dataframe(subject_stats, use_container_width=True)
                
            else:
                st.info("No subjects assigned to you yet. Please contact the administrator.")
                
    except Exception as e:
        st.error(f"Error loading marks data: {e}")
