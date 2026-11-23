
import streamlit as st
import pandas as pd
import joblib
import os
import time
import plotly.graph_objects as go
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="EduPredict AI",
    page_icon="🎓",
    layout="wide"
)

# PURPLE THEME
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #160D2B, #241343, #32195A);
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #1C1035;
}
h1, h2, h3, p, label {
    color: white !important;
}
.hero {
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(120deg,#7138C8,#A66BEE);
    text-align: center;
    margin-bottom: 25px;
}
.hero h1 {
    font-size: 42px;
}
.card {
    background: #352052;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #7046A5;
    text-align: center;
}
div.stButton > button {
    background: linear-gradient(90deg,#9147E8,#C084FC);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    padding: 12px;
}
div.stButton > button:hover {
    background: #B98AF5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# LOAD MODEL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "Model", "model.pkl")

model = joblib.load(MODEL_PATH)

# SIDEBAR
st.sidebar.title("🎓 EduPredict AI")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Prediction", "About"]
)

# HOME PAGE
if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🎓 Welcome to EduPredict AI</h1>
        <h3>Your Smart Student Performance Predictor</h3>
        <p>Discover academic potential using Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=900",
            use_container_width=True
        )

    with col2:
        st.subheader("✨ Smart Learning Starts Here")
        st.write("""
        EduPredict AI helps estimate student academic performance
        using important academic factors.

        Enter student details and get an instant prediction
        with visual performance analysis.
        """)
        st.success("AI Powered Student Performance Analysis")

    st.divider()

    st.subheader("🚀 Platform Features")

    a, b, c = st.columns(3)

    with a:
        st.markdown('<div class="card"><h2>📊</h2><h3>Smart Analytics</h3><p>Visual performance charts</p></div>', unsafe_allow_html=True)

    with b:
        st.markdown('<div class="card"><h2>🤖</h2><h3>AI Prediction</h3><p>Machine learning based score</p></div>', unsafe_allow_html=True)

    with c:
        st.markdown('<div class="card"><h2>💡</h2><h3>Study Suggestions</h3><p>Personalized improvement tips</p></div>', unsafe_allow_html=True)

    st.write("")
    if st.button("Start Prediction 🚀", use_container_width=True):
        st.session_state.page = "Prediction"
        st.rerun()

# PREDICTION PAGE
elif page == "Prediction":

    st.title("🔮 Student Performance Prediction")
    st.write("Enter academic details below.")

    col1, col2 = st.columns(2)

    with col1:
        study_hours = st.slider("📚 Study Hours", 0.0, 12.0, 5.0, 0.5)
        attendance = st.slider("📅 Attendance (%)", 0, 100, 80)

    with col2:
        assignments = st.slider("📝 Assignment Score", 0, 100, 75)
        previous_score = st.slider("📖 Previous Exam Score", 0, 100, 70)

    if st.button("✨ Predict My Score", use_container_width=True):

        input_data = pd.DataFrame({
            "StudyHours": [study_hours],
            "Attendance": [attendance],
            "Assignments": [assignments],
            "PreviousScore": [previous_score]
        })

        prediction = model.predict(input_data)
        score = float(prediction[0])

        st.divider()
        st.subheader("🏆 Your Prediction Result")

        score_placeholder = st.empty()

        # ANIMATED SCORE
        for value in range(0, int(score) + 1):
            score_placeholder.markdown(
                f"""
                <div class="hero">
                    <h3>Predicted Final Score</h3>
                    <h1>{value}/100</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.015)

        st.progress(max(0.0, min(1.0, score / 100)))

        # PERFORMANCE CATEGORY
        if score >= 80:
            st.success("🌟 Excellent Performance!")
            suggestion = "Keep maintaining your study routine and continue practicing."
        elif score >= 60:
            st.info("👍 Good Performance!")
            suggestion = "Increase revision time and practice more questions."
        elif score >= 40:
            st.warning("⚡ Average Performance")
            suggestion = "Improve attendance, study regularly and complete assignments on time."
        else:
            st.error("📚 Needs Improvement")
            suggestion = "Create a daily study plan, attend classes regularly and seek extra academic support."

        st.subheader("💡 Improvement Suggestions")
        st.write(suggestion)

        # INTERACTIVE CHART
        st.subheader("📊 Academic Performance Analysis")

        chart_data = pd.DataFrame({
            "Academic Factors": [
                "Study Hours",
                "Attendance",
                "Assignments",
                "Previous Score"
            ],
            "Values": [
                study_hours / 12 * 100,
                attendance,
                assignments,
                previous_score
            ]
        })

        fig = px.bar(
            chart_data,
            x="Academic Factors",
            y="Values",
            color="Academic Factors",
            text="Values",
            color_discrete_sequence=[
                "#A855F7", "#C084FC", "#7C3AED", "#E9D5FF"
            ],
            title="Student Academic Performance"
        )

        fig.update_layout(
            template="plotly_dark",
            yaxis_range=[0, 100],
            showlegend=False,
            paper_bgcolor="#241343",
            plot_bgcolor="#241343",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)

        # SCORE GAUGE
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Predicted Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#C084FC"},
                "steps": [
                    {"range": [0, 40], "color": "#512044"},
                    {"range": [40, 60], "color": "#7046A5"},
                    {"range": [60, 80], "color": "#8B5CF6"},
                    {"range": [80, 100], "color": "#A78BFA"}
                ]
            }
        ))

        gauge.update_layout(
            template="plotly_dark",
            paper_bgcolor="#241343",
            font_color="white"
        )

        st.plotly_chart(gauge, use_container_width=True)

# ABOUT PAGE
elif page == "About":

    st.title("ℹ️ About EduPredict AI")

    st.image(
        "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=1000",
        use_container_width=True
    )

    st.write("""
    EduPredict AI is a Machine Learning based student performance
    prediction application.

    It uses four academic factors:

    - Study Hours
    - Attendance
    - Assignment Score
    - Previous Exam Score

    The trained machine learning model estimates the student's
    final academic score.

    Project: Student Performance Prediction
    Technology: Python, Streamlit, Pandas, Scikit-learn
    """)

st.divider()
st.caption("🎓 EduPredict AI | Student Performance Prediction Project")
