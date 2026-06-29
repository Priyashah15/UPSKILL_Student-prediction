import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("model/model.pkl")

st.set_page_config(page_title="Student Performance Predictor")

st.title("🎓 Student Performance Prediction")

st.write("Enter the student's details below.")

study_hours = st.number_input("Study Hours", min_value=0.0, max_value=12.0, value=5.0)
attendance = st.number_input("Attendance (%)", min_value=0, max_value=100, value=80)
assignments = st.number_input("Assignment Score", min_value=0, max_value=100, value=75)
previous_score = st.number_input("Previous Exam Score", min_value=0, max_value=100, value=70)

if st.button("Predict Final Score"):

    input_data = pd.DataFrame({
        "StudyHours":[study_hours],
        "Attendance":[attendance],
        "Assignments":[assignments],
        "PreviousScore":[previous_score]
    })

    prediction = model.predict(input_data)

    st.success(f"Predicted Final Score: {prediction[0]:.2f}")