
import streamlit as st
import pandas as pd
import joblib
import os
import time
import plotly.express as px
import plotly.graph_objects as go

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="wide"
)

# PINK AND PURPLE THEME
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #24072F, #50104F, #781B67, #321044);
    color: #FFD6F5;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #351044, #70205F, #4B155C);
}

h1, h2, h3, h4, p, label {
    color: #FFD6F5 !important;
}

.hero {
    background: linear-gradient(120deg, #8E287F, #D946A6, #9235B8);
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    border: 2px solid #F472C5;
}

.card {
    background: linear-gradient(135deg, #65205F, #A32C83);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #E879C9;
}

/* NORMAL BUTTON */
div.stButton > button {
    background: linear-gradient(90deg, #C02691, #9333EA, #DB2777) !important;
    color: #FFE4F5 !important;
    border: 1px solid #F472C5 !important;
    border-radius: 14px !important;
    font-weight: bold !important;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #DB2777, #A855F7) !important;
}

/* PDF DOWNLOAD BUTTON - WHITE BACKGROUND FIX */
div.stDownloadButton > button,
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(90deg, #C02691, #9333EA, #DB2777) !important;
    background-color: #9333EA !important;
    color: #FFE4F5 !important;
    border: 2px solid #F472C5 !important;
    border-radius: 14px !important;
    font-weight: bold !important;
    padding: 12px 20px !important;
    box-shadow: 0 4px 12px rgba(219, 39, 119, 0.3) !important;
}

div.stDownloadButton > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(90deg, #DB2777, #A855F7) !important;
    background-color: #DB2777 !important;
    color: white !important;
    border: 2px solid #F9A8D4 !important;
}

div.stDownloadButton > button p,
div[data-testid="stDownloadButton"] > button p {
    color: #FFE4F5 !important;
    font-weight: bold !important;
}

/* PROGRESS BAR */
[data-testid="stProgressBar"] > div {
    background: #65205F;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #DB2777, #C084FC);
}

/* ALERT */
[data-testid="stAlert"] {
    background: linear-gradient(120deg, #581C65, #9D267D) !important;
    border: 2px solid #D946A6 !important;
    border-radius: 15px;
}

[data-testid="stAlert"] p {
    color: #FFD6F5 !important;
}

hr {
    border-color: #C02691;
}
</style>
""", unsafe_allow_html=True)


# LOAD TRAINED MODEL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "Model", "model.pkl")
model = joblib.load(MODEL_PATH)


# PDF REPORT FUNCTION
def create_pdf_report(
    study_hours,
    attendance,
    assignments,
    previous_score,
    score,
    performance,
    suggestion
):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFillColorRGB(0.15, 0.03, 0.22)
    pdf.rect(0, 0, 595, 842, fill=1)

    pdf.setFillColorRGB(0.95, 0.45, 0.75)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(297, 790, "Student Performance Report")

    pdf.setFillColorRGB(1, 0.82, 0.94)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(55, 725, "Prediction Result")

    pdf.setFont("Helvetica-Bold", 32)
    pdf.drawString(55, 675, f"{score:.2f}/100")

    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(55, 625, performance)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(55, 565, "Academic Details")

    pdf.setFont("Helvetica", 12)

    details = [
        f"Study Hours: {study_hours}",
        f"Attendance: {attendance}%",
        f"Assignment Score: {assignments}",
        f"Previous Exam Score: {previous_score}"
    ]

    y = 530
    for detail in details:
        pdf.drawString(65, y, detail)
        y -= 30

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(55, 375, "Improvement Suggestions")

    pdf.setFont("Helvetica", 11)
    y = 345

    for line in suggestion.split("\n"):
        if line.strip():
            pdf.drawString(65, y, line.strip())
            y -= 22

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawCentredString(
        297, 60,
        "Student Performance Prediction System"
    )

    pdf.save()
    buffer.seek(0)

    return buffer.getvalue()


# SIDEBAR NAVIGATION
st.sidebar.title("🎓 Student Prediction")

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
        st.subheader("Welcome to Our System")

        st.write("""
        Our Student Performance Prediction System
        uses Machine Learning to estimate student
        academic performance.

        Enter student details and receive an instant
        prediction with interactive visual analysis.

        Discover academic strengths and areas
        that need improvement.
        """)

        st.markdown("""
        <div class="card">
            <h3>💗 AI Powered Academic Analysis</h3>
            <p>Smart prediction for better learning.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("✨ Our Features")

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card">
            <h2>📊</h2>
            <h3>Smart Analytics</h3>
            <p>Interactive performance charts</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
            <h2>🤖</h2>
            <h3>AI Prediction</h3>
            <p>Machine Learning based prediction</p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card">
            <h2>💡</h2>
            <h3>Smart Suggestions</h3>
            <p>Academic improvement tips</p>
        </div>
        """, unsafe_allow_html=True)


# PREDICTION PAGE
elif page == "Prediction":

    st.title("🔮 Student Performance Prediction")

    st.write("Enter the student's academic details below.")

    col1, col2 = st.columns(2)

    with col1:
        study_hours = st.slider(
            "📚 Study Hours", 0.0, 12.0, 5.0, 0.5
        )

        attendance = st.slider(
            "📅 Attendance (%)", 0, 100, 80
        )

    with col2:
        assignments = st.slider(
            "📝 Assignment Score", 0, 100, 75
        )

        previous_score = st.slider(
            "📖 Previous Exam Score", 0, 100, 70
        )

    st.write("")

    if st.button("✨ Predict Final Score", use_container_width=True):

        input_data = pd.DataFrame({
            "StudyHours": [study_hours],
            "Attendance": [attendance],
            "Assignments": [assignments],
            "PreviousScore": [previous_score]
        })

        prediction = model.predict(input_data)
        score = float(prediction[0])

        st.divider()
        st.subheader("🏆 Prediction Result")

        # ANIMATED SCORE
        score_placeholder = st.empty()
        target = max(0, min(100, int(score)))

        for value in range(target + 1):
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

        # PERFORMANCE ANALYSIS
        st.subheader("💗 Performance Analysis")

        if score >= 80:
            performance = "Excellent Performance!"
            suggestion = (
                "Keep maintaining your study routine. "
                "Continue practicing and revising regularly."
            )
            color = "#DB2777"

        elif score >= 60:
            performance = "Good Performance!"
            suggestion = (
                "Increase revision time and practice "
                "more questions to improve your score."
            )
            color = "#C026D3"

        elif score >= 40:
            performance = "Average Performance"
            suggestion = (
                "Improve attendance, complete assignments "
                "regularly and follow a daily study schedule."
            )
            color = "#9333EA"

        else:
            performance = "Needs Improvement"
            suggestion = (
                "Focus on regular study, attend classes "
                "and seek additional academic support."
            )
            color = "#BE185D"

        # PERFORMANCE CARD
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(120deg, #581C65, #9D267D, #701A75);
                border: 2px solid {color};
                border-radius: 20px;
                padding: 28px;
                text-align: center;
                margin: 15px 0;
            ">
                <h2 style="color: #FFD6F5 !important; font-size: 27px;">
                    💗 {performance}
                </h2>
                <p style="color: #FFD6F5 !important; font-size: 17px;">
                    {suggestion}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # PDF DOWNLOAD
        st.subheader("📄 Download Your Report")

        pdf_file = create_pdf_report(
            study_hours,
            attendance,
            assignments,
            previous_score,
            score,
            performance,
            suggestion
        )

        st.download_button(
            label="💗 Download Prediction Report (PDF)",
            data=pdf_file,
            file_name="Student_Performance_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="pdf_download"
        )

        st.divider()

        # BAR CHART
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

        colors = [
            "#EC4899",
            "#D946EF",
            "#A855F7",
            "#F472B6"
        ]

        fig = px.bar(
            chart_data,
            x="Academic Factors",
            y="Values",
            text="Values",
            color="Academic Factors",
            color_discrete_sequence=colors
        )

        fig.update_traces(
            texttemplate="%{y:.1f}",
            textposition="outside",
            textfont=dict(
                color="#FFD6F5",
                size=15
            ),
            marker_line_width=0
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#351044",
            plot_bgcolor="#351044",
            font=dict(
                color="#FFD6F5",
                size=14
            ),
            yaxis=dict(
                range=[0, 115],
                title="Performance (%)",
                gridcolor="#70205F"
            ),
            xaxis=dict(title="Academic Factors"),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # SCORE GAUGE
        st.subheader("🎯 Final Score Gauge")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={
                    "text": "Predicted Score",
                    "font": {"color": "#FFD6F5"}
                },
                number={
                    "font": {"color": "#F472B6"}
                },
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickcolor": "#FFD6F5"
                    },
                    "bar": {"color": "#EC4899"},
                    "bgcolor": "#351044",
                    "bordercolor": "#D946A6",
                    "steps": [
                        {"range": [0, 40], "color": "#581C48"},
                        {"range": [40, 60], "color": "#861F69"},
                        {"range": [60, 80], "color": "#A21CAF"},
                        {"range": [80, 100], "color": "#7E22CE"}
                    ]
                }
            )
        )

        gauge.update_layout(
            paper_bgcolor="#351044",
            font_color="#FFD6F5"
        )

        st.plotly_chart(gauge, use_container_width=True)

        # STUDENT DETAILS
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

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )


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

    The system uses four academic factors:

    - Study Hours
    - Attendance
    - Assignment Score
    - Previous Exam Score

    Technologies Used:

    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - Plotly
    - ReportLab
    """)


# FOOTER
st.divider()

st.caption(
    "🎓 Student Performance Prediction System | College Project"
)
