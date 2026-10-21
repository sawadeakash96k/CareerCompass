import streamlit as st
import pandas as pd
import plotly.express as px

from src.recommender import recommend_careers


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="CareerCompass | Find Your Direction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #0B1020;
        --panel: #131B2E;
        --indigo: #818CF8;
        --cyan: #67E8F9;
        --muted: #A6B0C5;
        --text: #F3F6FF;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 10% 0%, #1C2450 0%, transparent 35%),
            radial-gradient(ellipse at 95% 25%, #102F43 0%, transparent 30%),
            var(--navy);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        font-family: 'Inter', sans-serif !important;
    }

    h2, h3 {
        color: var(--text) !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #CBD5E1;
    }

    .hero {
        padding: 38px 30px;
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 24px;
        background: linear-gradient(
            125deg,
            rgba(79, 70, 229, 0.24),
            rgba(8, 145, 178, 0.12),
            rgba(19, 27, 46, 0.8)
        );
        margin-bottom: 24px;
    }

    .brand {
        color: var(--cyan);
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: clamp(32px, 5vw, 54px);
        line-height: 1.12;
        font-weight: 800;
        letter-spacing: -1.8px;
        margin: 0 0 16px 0;
    }

    .gradient-text {
        background: linear-gradient(90deg, #A5B4FC, #67E8F9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        color: #CBD5E1;
        font-size: 16px;
        line-height: 1.8;
        max-width: 700px;
        margin-bottom: 20px;
    }

    .hero-tag {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px 6px 0 0;
        border-radius: 20px;
        border: 1px solid rgba(165, 180, 252, 0.3);
        background: rgba(129, 140, 248, 0.10);
        color: #E0E7FF;
        font-size: 12px;
        font-weight: 600;
    }

    .section-kicker {
        color: var(--cyan);
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }

    .section-heading {
        font-size: 27px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 5px;
    }

    .section-description {
        color: var(--muted);
        font-size: 14px;
        margin-bottom: 20px;
    }

    [data-testid="stForm"] {
        background: rgba(19, 27, 46, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 20px;
        padding: 24px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(148, 163, 184, 0.22) !important;
        border-radius: 18px !important;
        background: rgba(19, 27, 46, 0.72);
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #10182A;
        border-color: #35415C;
        border-radius: 10px;
    }

    div[data-testid="stTextInput"] input {
        background: #10182A;
        border: 1px solid #35415C;
        border-radius: 10px;
        color: #FFFFFF;
    }

    .stButton button,
    .stFormSubmitButton button,
    .stDownloadButton button {
        border-radius: 11px;
        min-height: 46px;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    .stFormSubmitButton button,
    .stDownloadButton button {
        background: linear-gradient(100deg, #6366F1, #0891B2);
        color: #FFFFFF;
        border: none;
    }

    .stButton button:hover,
    .stFormSubmitButton button:hover,
    .stDownloadButton button:hover {
        border-color: #67E8F9;
        color: #FFFFFF;
        filter: brightness(1.12);
    }

    .result-name {
        color: #FFFFFF;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .match-label {
        display: inline-block;
        background: rgba(103, 232, 249, 0.10);
        border: 1px solid rgba(103, 232, 249, 0.28);
        color: #A5F3FC;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 700;
    }

    .profile-chip {
        background: rgba(129, 140, 248, 0.09);
        border: 1px solid rgba(129, 140, 248, 0.22);
        border-radius: 12px;
        padding: 13px;
        margin-bottom: 8px;
    }

    .profile-label {
        color: #94A3B8;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .profile-value {
        color: #F8FAFC;
        font-size: 15px;
        font-weight: 700;
        margin-top: 5px;
    }

    .footer {
        border-top: 1px solid rgba(148, 163, 184, 0.2);
        padding-top: 22px;
        margin-top: 38px;
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.8;
    }

    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 25px 18px;
        }

        .hero-title {
            letter-spacing: -1px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD CAREER DATA
# --------------------------------------------------
@st.cache_data
def load_careers():
    return pd.read_csv("data/careers.csv")


careers_df = load_careers()


# --------------------------------------------------
# CAREER ROADMAPS
# --------------------------------------------------
skill_roadmaps = {
    "Software Developer": [
        "Python or Java",
        "Data Structures and Algorithms",
        "Git and GitHub",
        "SQL and databases",
    ],
    "Data Scientist": [
        "Python",
        "Statistics and probability",
        "Pandas and data visualization",
        "Machine learning",
    ],
    "Cybersecurity Analyst": [
        "Networking fundamentals",
        "Linux basics",
        "Security fundamentals",
        "Log analysis",
    ],
    "Web Developer": [
        "HTML and CSS",
        "JavaScript",
        "Responsive web design",
        "Git and GitHub",
    ],
    "AI Engineer": [
        "Python",
        "Linear algebra and statistics",
        "Machine learning",
        "Deep learning fundamentals",
    ],
}

project_ideas = {
    "Software Developer": [
        "Build a task management application",
        "Create a student record system",
        "Develop a REST API",
    ],
    "Data Scientist": [
        "Analyze a public dataset",
        "Build a data visualization dashboard",
        "Create a simple prediction model",
    ],
    "Cybersecurity Analyst": [
        "Build a password strength analyzer",
        "Analyze sample security logs",
        "Create a basic file integrity checker",
    ],
    "Web Developer": [
        "Build a personal portfolio website",
        "Create a responsive landing page",
        "Develop a simple blog website",
    ],
    "AI Engineer": [
        "Build a basic chatbot",
        "Create a text classification model",
        "Develop an image classification prototype",
    ],
}


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="brand">✦ CareerCompass</div>
        <div class="hero-title">
            Your future.<br>
            <span class="gradient-text">Your direction.</span>
        </div>
        <div class="hero-description">
            Discover career paths that align with your interests,
            skills, education, and working style. Get personalized
            recommendations and a practical roadmap to take your next step.
        </div>
        <span class="hero-tag">✦ Personalized Matches</span>
        <span class="hero-tag">↗ Skills Roadmaps</span>
        <span class="hero-tag">⌘ Project Ideas</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# STUDENT PROFILE FORM
# --------------------------------------------------
st.markdown(
    """
    <div class="section-kicker">Start your journey</div>
    <div class="section-heading">Let's discover your potential.</div>
    <div class="section-description">
        Tell us a little about yourself to explore careers that match your profile.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("career_profile_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Your name (optional)",
            placeholder="Enter your name",
        )

        stream = st.selectbox(
            "Academic stream",
            ["Science", "Commerce", "Arts", "Any"],
        )

        interest = st.selectbox(
            "Main interest",
            sorted(careers_df["interest"].unique()),
        )

    with col2:
        skill = st.selectbox(
            "Strongest skill",
            sorted(careers_df["skill"].unique()),
        )

        work_style = st.selectbox(
            "Preferred work style",
            sorted(careers_df["work_style"].unique()),
        )

    submitted = st.form_submit_button(
        "✦ Discover My Career Matches",
        use_container_width=True,
    )


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------
if submitted:
    student_profile = {
        "stream": stream,
        "interest": interest,
        "skill": skill,
        "work_style": work_style,
    }

    recommendations = recommend_careers(
        student_profile,
        careers_df,
        top_n=5,
    )

    st.divider()

    if name.strip():
        st.markdown(
            f"### Welcome, {name.strip()}! 👋",
        )
    else:
        st.markdown("### Your career exploration starts here. 👋")

    # Profile summary
    st.markdown(
        """
        <div class="section-kicker">Your profile</div>
        <div class="section-heading">A snapshot of you.</div>
        """,
        unsafe_allow_html=True,
    )

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    profile_items = [
        (summary_col1, "Academic stream", stream),
        (summary_col2, "Main interest", interest),
        (summary_col3, "Strongest skill", skill),
        (summary_col4, "Work style", work_style),
    ]

    for column, label, value in profile_items:
        with column:
            st.markdown(
                f"""
                <div class="profile-chip">
                    <div class="profile-label">{label}</div>
                    <div class="profile-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Personalized guidance
    if not recommendations.empty:
        top_career = recommendations.iloc[0]["career"]

        st.success(
            f"🎯 Your strongest rule-based match is **{top_career}**. "
            "Explore its skills, qualifications, and career opportunities."
        )

    # Score explanation
    st.info(
        "📌 **How scores work:** Academic stream matches add 2 points, "
        "interest matches add 3 points, skill matches add 3 points, "
        "and work-style matches add 2 points. Scores measure profile "
        "matches against this sample dataset; they are not probabilities "
        "of career success."
    )

    # Chart
    st.markdown(
        """
        <div class="section-kicker">Your results</div>
        <div class="section-heading">Career matches, visualized.</div>
        <div class="section-description">
            Compare the match scores for your top five suggested careers.
        </div>
        """,
        unsafe_allow_html=True,
    )

    chart_data = recommendations.sort_values(
        by="score",
        ascending=True,
    )

    fig = px.bar(
        chart_data,
        x="score",
        y="career",
        orientation="h",
        text="score",
        color="score",
        color_continuous_scale=[
            "#312E81",
            "#6366F1",
            "#22D3EE",
        ],
        labels={
            "score": "Match score",
            "career": "Career",
        },
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color="#E2E8F0",
        ),
        xaxis=dict(
            title="Match score out of 10",
            range=[0, 11.5],
            dtick=2,
            gridcolor="rgba(148,163,184,0.15)",
            zeroline=False,
        ),
        yaxis=dict(
            title="",
            categoryorder="total ascending",
        ),
        coloraxis_showscale=False,
        margin=dict(l=10, r=30, t=20, b=20),
        height=340,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    # Career cards
    st.markdown(
        """
        <div class="section-kicker">Explore your options</div>
        <div class="section-heading">Your top career paths.</div>
        <div class="section-description">
            Open any career to explore its details, learning roadmap, and project ideas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    for rank, (_, career) in enumerate(
        recommendations.iterrows(),
        start=1,
    ):
        score = int(career["score"])
        career_name = career["career"]

        with st.container(border=True):
            title_col, score_col = st.columns([3, 1])

            with title_col:
                st.markdown(
                    f'<div class="result-name">'
                    f'{rank:02d} &nbsp; {career_name}</div>',
                    unsafe_allow_html=True,
                )

            with score_col:
                st.markdown(
                    f'<div class="match-label">'
                    f'{score}/10 MATCH SCORE</div>',
                    unsafe_allow_html=True,
                )

            st.progress(
                max(0, min(score, 10)) / 10,
                text=f"Profile match: {score} out of 10",
            )

            st.write(career["description"])

            with st.expander("Explore career details and roadmap"):
                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.markdown("**🎓 Career profile**")
                    st.write(f"**Stream:** {career['stream']}")
                    st.write(f"**Interest:** {career['interest']}")

                with detail_col2:
                    st.markdown("**🧭 Your profile match**")
                    st.write(f"**Key skill:** {career['skill']}")
                    st.write(f"**Work style:** {career['work_style']}")

                st.divider()

                # Skills roadmap
                st.markdown("**🛠️ Suggested skills roadmap**")

                roadmap = skill_roadmaps.get(
                    career_name,
                    [
                        f"Build foundational knowledge in {career['interest']}",
                        f"Improve your {career['skill']} skills",
                        "Complete a practical project",
                        "Explore relevant courses and certifications",
                    ],
                )

                for roadmap_skill in roadmap:
                    st.write(f"☐ {roadmap_skill}")

                st.divider()

                # Practical projects
                st.markdown("**💡 Projects to build**")

                ideas = project_ideas.get(
                    career_name,
                    [
                        f"Create a beginner project related to {career['interest']}",
                        "Build a small practical application",
                        "Document your project on GitHub",
                    ],
                )

                for idea in ideas:
                    st.write(f"• {idea}")

    # Download results
    st.markdown("### 📥 Take your results with you")

    csv_data = recommendations.to_csv(
        index=False,
    ).encode("utf-8-sig")

    st.download_button(
        label="Download My Career Recommendations (CSV)",
        data=csv_data,
        file_name="career_recommendations.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.caption(
        "Career suggestions are for educational exploration. "
        "Consider your qualifications, goals, and interests before making decisions."
    )

    if st.button(
        "↻ Start a New Career Search",
        use_container_width=True,
    ):
        st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <strong style="color:#A5B4FC;">✦ CareerCompass</strong><br>
        Find your direction. Build your future.<br>
        Student Career Recommendation System · Educational guidance prototype
    </div>
    """,
    unsafe_allow_html=True,
)