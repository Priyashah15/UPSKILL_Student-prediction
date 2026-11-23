import streamlit as st
import pandas as pd
import joblib
import os

# Page Configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
}
.main-title {
    text-align: center;
    color: #17365D;
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #64748B;
    font-size: 17px;
}
.result-card {
    background-color: #FFFFFF;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #DCE5F0;
}
.result-score {
    color: #17365D;
    font-size: 42px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Load Model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "Model", "model.pkl")

model = joblib.load(MODEL_PATH)

# Header
st.markdown(
    '<div class="main-title">🎓 Student Performance Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Machine Learning Based Academic Performance Analysis</div>',
    unsafe_allow_html=True
)

st.divider()

st.subheader("📋 Student Information")
st.write("Enter the student's academic details to predict the final score.")

# Input Section
col1, col2 = st.columns(2)

with col1:
    study_hours = st.number_input(
        "📚 Study Hours per Day",
        min_value=0.0,
        max_value=12.0,
        value=5.0
    )

    attendance = st.number_input(
        "📅 Attendance (%)",
        min_value=0,
        max_value=100,
        value=80
    )

with col2:
    assignments = st.number_input(
        "📝 Assignment Score",
        min_value=0,
        max_value=100,
        value=75
    )

    previous_score = st.number_input(
        "📊 Previous Exam Score",
        min_value=0,
        max_value=100,
        value=70
    )

st.divider()

# Prediction
if st.button("🔍 Predict Final Score", use_container_width=True):

    input_data = pd.DataFrame({
        "StudyHours": [study_hours],
        "Attendance": [attendance],
        "Assignments": [assignments],
        "PreviousScore": [previous_score]
    })

    prediction = model.predict(input_data)
    score = float(prediction[0])

    st.subheader("📊 Prediction Result")

    st.markdown(f"""
    <div class="result-card">
        <p style="color:#64748B;font-size:18px;">
            Predicted Final Score
        </p>
        <div class="result-score">{score:.2f}</div>
        <p style="color:#64748B;">Machine Learning Prediction</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(max(0.0, min(1.0, score / 100)))

    st.subheader("📈 Performance Analysis")

    if score >= 80:
        st.success("Excellent performance! Keep up the good work.")
    elif score >= 60:
        st.info("Good performance! Continue improving your studies.")
    elif score >= 40:
        st.warning("Average performance. More practice is recommended.")
    else:
        st.error("Needs improvement. Focus on regular study and practice.")

    st.subheader("📋 Student Details")

    result_df = pd.DataFrame({
        "Parameter": [
            "Study Hours",
            "Attendance",
            "Assignment Score",
            "Previous Exam Score"
        ],
        "Value": [
            study_hours,
            f"{attendance}%",
            assignments,
            previous_score
        ]
    })

    st.dataframe(result_df, use_container_width=True)

st.divider()

st.caption("Student Performance Predictor | Machine Learning College Project")
