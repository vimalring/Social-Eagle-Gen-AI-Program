import streamlit as st
import pandas as pd

st.title("🎓 Student Grade Manager")

if "students" not in st.session_state:
    st.session_state.students = []

name = st.text_input("Student Name")

mark = st.number_input(
    "Student Mark",
    min_value=0,
    max_value=100,
    value=0
)

def calculate_grade(mark):
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"

if st.button("Add Student"):
    if name.strip() == "":
        st.error("Please enter a student name.")
    else:
        grade = calculate_grade(mark)

        st.session_state.students.append({
            "Name": name,
            "Mark": mark,
            "Grade": grade
        })

        st.success(f"{name} added successfully!")

if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    st.subheader("Student Records")
    st.dataframe(df)

    st.write(f"Average Mark: {df['Mark'].mean():.2f}")