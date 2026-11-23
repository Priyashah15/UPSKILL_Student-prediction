import streamlit as st
import pandas as pd
import joblib
import os
import time
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#160D2B,#241343,#32195A);
    color: white;
}
[data-testid="stSidebar"] {
    background: #1C1035;
}
h1,h2,h3,p,label {
    color: white !important;
}
.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(120deg,#7138C8,#A66BEE);
    text-align: center;
}
.card {
    background: #352052;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #7046A5;
}
div.stButton > button {
    background: linear-gradient(90deg,#9147E8,#C084FC);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# LOAD MODEL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "Model", "model.pkl")
model = joblib.load(MODEL_PATH)

# NAVIGATION
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Prediction", "About"]
)

# HOME PAGE
if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🎓 Student Performance Prediction System</h1>
        <h3>Machine Learning Based Academic Analysis</h3>
        <p>Predict student performance and discover academic potential.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=900",
            use_container_width=True
        )

    with col2:
        st.subheader("Welcome to Student Performance Prediction")
        st.write("""
        This system uses Machine Learning to estimate
        student academic performance.

        Enter academic details and get an instant prediction
        with interactive visual analysis.
        """)
        st.success("AI Powered Academic Analysis")

    st.divider()

    st.subheader("Our Features")

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            '<div class="card"><h2>📊</h2><h3>Analytics</h3><p>Interactive charts</p></div>',
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            '<div class="card"><h2>🤖</h2><h3>Prediction</h3><p>Machine Learning model</p></div>',
            unsafe_allow_html=True
        )

    with c:
        st.markdown(
            '<div class="card"><h2>💡</h2><h3>Suggestions</h3><p>Academic improvement tips</p></div>',
            unsafe_allow_html=True
        )

# PREDICTION PAGE
elif page == "Prediction":

    st.title("🔮 Student Performance Prediction")
    st.write("Enter student academic details below.")

    col1, col2 = st.columns(2)

    with col1:
        study_hours = st.slider("📚 Study Hours", 0.0, 12.0, 5.0, 0.5)
        attendance = st.slider("📅 Attendance (%)", 0, 100, 80)

    with col2:
        assignments = st.slider("📝 Assignment Score", 0, 100, 75)
        previous_score = st.slider("📖 Previous Exam Score", 0, 100, 70)

    if st.button("✨ Predict Final Score", use_container_width=True):

        input_data = pd.DataFrame({
            "StudyHours": [study_hours],
            "Attendance": [attendance],
            "Assignments": [assignments],
            "PreviousScore": [previous_score]
        })

        score = float(model.predict(input_data)[0])

        st.divider()
        st.subheader("🏆 Prediction Result")

        score_placeholder = st.empty()

        for value in range(0, max(1, int(score)) + 1):
            score_placeholder.markdown(
                f"""
                <div class="hero">
                    <h3>Predicted Final Score</h3>
                    <h1>{value:.0f}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.015)

        st.progress(max(0.0, min(1.0, score / 100)))

        if score >= 80:
            st.success("🌟 Excellent Performance!")
            suggestion = "Maintain your study routine and continue practicing."
        elif score >= 60:
            st.info("👍 Good Performance!")
            suggestion = "Increase revision time and practice more questions."
        elif score >= 40:
            st.warning("⚡ Average Performance")
            suggestion = "Improve attendance and complete assignments regularly."
        else:
            st.error("📚 Needs Improvement")
            suggestion = "Follow a daily study plan and seek extra academic support."

        st.subheader("💡 Improvement Suggestions")
        st.write(suggestion)

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
    text="Values",
    color_discrete_sequence=["#C084FC"]
)

fig.update_traces(
    marker_line_color="#E9D5FF",
    marker_line_width=1,
    textfont_color="white"
)
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            yaxis_range=[0, 100],
            showlegend=False,
            paper_bgcolor="#241343",
            plot_bgcolor="#241343"
        )

        st.plotly_chart(fig, use_container_width=True)

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

    st.title("ℹ️ About Our Project")

    st.image(
        "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=1000",
        use_container_width=True
    )

    st.write("""
    Student Performance Prediction System is a
    Machine Learning based academic prediction application.

    It uses four academic factors:

    - Study Hours
    - Attendance
    - Assignment Score
    - Previous Exam Score

    Technology Used:
    Python, Streamlit, Pandas, Scikit-learn and Plotly.
    """)

st.divider()
st.caption("🎓 Student Performance Prediction System | College Project")
