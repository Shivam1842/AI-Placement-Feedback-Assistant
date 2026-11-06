import streamlit as st

from graph import app as workflow_app
from nodes import generate_interview_question


st.set_page_config(
    page_title="PlacementSathi | Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROLE_OPTIONS = [
    "Python Developer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Full Stack Developer",
    "AI Engineer",
    "Software Developer",
    "Data Analyst",
    "Cloud Engineer",
]

DEFAULTS = {
    "generated_question_input": "",
    "generated_for_role": "",
    "custom_question": "",
    "student_answer": "",
    "result": None,
    "total_attempts": 0,
    "resume_upload_version": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_interview():
    st.session_state.generated_question_input = ""
    st.session_state.generated_for_role = ""
    st.session_state.custom_question = ""
    st.session_state.student_answer = ""
    st.session_state.result = None
    st.session_state.question_mode = "✨ Generate with AI"
    st.session_state.resume_upload_version += 1


def local_css():
    st.markdown(
        """
    <style>
    :root {
        color-scheme: dark;
        --space: #0E1117;
        --slate: #161A25;
        --ice: #FAFAFA;
        --muted: #9BA8BA;
        --cyan: #00F0FF;
        --violet: #8A2BE2;
        --glass: rgba(22, 26, 37, 0.72);
        --line: rgba(148, 163, 184, 0.16);
    }

    .stApp,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 82% 0%, rgba(52, 33, 99, 0.22), transparent 34%),
            radial-gradient(ellipse at 8% 18%, rgba(0, 240, 255, 0.07), transparent 30%),
            #0E1117 !important;
        color: #FAFAFA !important;
    }

    p, span, div, label, h1, h2, h3 {
        color: #FAFAFA !important;
    }

    h1 {
        background: linear-gradient(90deg, #00F0FF 0%, #A6F8FF 48%, #8A2BE2 100%) !important;
        background-clip: text !important;
        -webkit-background-clip: text !important;
        color: transparent !important;
        -webkit-text-fill-color: transparent !important;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] *,
    .stRadio label,
    div[role="radiogroup"] label,
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploadDropzone"] *,
    p,
    span {
        color: #FAFAFA !important;
    }

    [data-testid="stHeader"], #MainMenu, footer {
        display: none;
    }

    .block-container {
        max-width: 1680px;
        padding: 0.9rem 2rem 2.5rem;
    }

    section[data-testid="stSidebar"] {
        background: rgba(16, 20, 30, 0.82) !important;
        border-right: 1px solid var(--line);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.4rem;
    }

    .brand-mark {
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: var(--ice);
    }

    .brand-mark span {
        color: var(--cyan) !important;
    }

    .brand-caption, .muted-copy {
        color: var(--muted);
        font-size: 0.88rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: clamp(1.5rem, 4vw, 2.6rem);
        margin: 0.7rem 0 2rem;
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 24px;
        background:
            linear-gradient(118deg, rgba(22, 26, 37, 0.94), rgba(20, 25, 41, 0.72)),
            radial-gradient(circle at 90% 15%, rgba(138, 43, 226, 0.24), transparent 42%);
        box-shadow: 0 22px 70px rgba(0, 0, 0, 0.24);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -85px;
        top: -125px;
        border-radius: 50%;
        background: rgba(0, 240, 255, 0.12);
        filter: blur(45px);
        pointer-events: none;
    }

    .hero-kicker, .eyebrow {
        color: var(--cyan) !important;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .hero h1 {
        margin: 0.55rem 0 0.6rem;
        font-size: clamp(2rem, 4vw, 3.15rem);
        font-weight: 850;
        line-height: 1.08;
        letter-spacing: -0.055em;
    }

    .hero p {
        max-width: 610px;
        margin: 0;
        color: #B8C2D2;
        font-size: 1rem;
        line-height: 1.7;
    }

    .section-heading {
        margin: 0.35rem 0 0.25rem;
        color: var(--ice);
        font-size: 1.55rem;
        font-weight: 760;
        letter-spacing: -0.035em;
    }

    .section-copy {
        margin-bottom: 1.35rem;
        color: var(--muted);
        line-height: 1.65;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--line);
        border-radius: 18px;
        background: var(--glass);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }

    div[data-testid="stMetric"] {
        min-height: 112px;
        padding: 1rem 1.15rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(28, 34, 49, 0.88), rgba(19, 23, 34, 0.82));
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.14);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }

    div[data-testid="stMetricLabel"] p {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"] {
        color: var(--ice);
    }

    .stButton > button,
    .stDownloadButton > button {
        min-height: 2.8rem;
        border-radius: 11px;
        font-weight: 680;
        transition: border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
        background-color: #161A25 !important;
        color: #FAFAFA !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: #00F0FF !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1);
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] {
        border: 1px solid rgba(0, 240, 255, 0.52);
        background: linear-gradient(105deg, rgba(0, 169, 190, 0.95), rgba(106, 52, 186, 0.95)) !important;
        color: #FFFFFF !important;
        box-shadow: 0 8px 26px rgba(0, 197, 218, 0.16);
    }

    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button:hover {
        border-color: #00F0FF !important;
        box-shadow: 0 0 22px rgba(0, 240, 255, 0.28);
        transform: translateY(-1px);
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        border: 1px solid #333 !important;
        border-radius: 12px;
        background: rgba(22, 26, 37, 0.7) !important;
        color: #FAFAFA !important;
    }

    div[data-baseweb="textarea"] textarea::placeholder,
    div[data-baseweb="input"] input::placeholder {
        color: #888888 !important;
        opacity: 1 !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: rgba(0, 240, 255, 0.6);
        box-shadow: 0 0 0 1px rgba(0, 240, 255, 0.22);
    }

    [data-testid="stFileUploadDropzone"] {
        background: #161A25 !important;
        border: 1px dashed #00F0FF !important;
        color: #FAFAFA !important;
    }

    [data-testid="stFileUploadDropzone"] *,
    [data-testid="stFileUploadDropzone"] svg {
        color: #FAFAFA !important;
        fill: #FAFAFA !important;
    }

    .stRadio label,
    .stCheckbox label,
    div[role="radiogroup"] label {
        color: #FAFAFA !important;
    }

    input[type="radio"],
    input[type="checkbox"] {
        accent-color: #00F0FF !important;
    }

    div[data-baseweb="select"] > div {
        border: 1px solid #333 !important;
        border-radius: 11px;
        background: rgba(22, 26, 37, 0.7) !important;
        color: #FAFAFA !important;
    }

    div[data-baseweb="popover"],
    ul[role="listbox"],
    li[role="option"] {
        background: #161A25 !important;
        color: #FAFAFA !important;
    }

    div[role="radiogroup"] {
        gap: 0.65rem;
    }

    div[data-testid="stChatMessage"] {
        margin: 0.75rem 0;
        padding: 1.1rem 1.2rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 16px;
        background: rgba(22, 26, 37, 0.72);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }

    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-color: rgba(0, 240, 255, 0.2);
        background: linear-gradient(120deg, rgba(0, 240, 255, 0.075), rgba(22, 26, 37, 0.82) 48%);
    }

    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-color: rgba(138, 43, 226, 0.25);
        background: linear-gradient(120deg, rgba(138, 43, 226, 0.1), rgba(22, 26, 37, 0.86) 52%);
    }

    .footer {
        padding: 2rem 0 0.5rem;
        color: #7F8A9B;
        font-size: 0.78rem;
        line-height: 1.8;
        text-align: center;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 0.55rem 1rem 2rem;
        }

        .hero {
            margin-top: 0.3rem;
            border-radius: 18px;
        }

        .hero p {
            font-size: 0.93rem;
        }

        div[data-testid="stChatMessage"] {
            padding: 0.85rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


local_css()


with st.sidebar:
    st.markdown(
        '<div class="brand-mark">✦ Placement<span>Sathi</span></div>'
        '<div class="brand-caption">Your personal interview coach</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "Workspace",
        ["🏠 Interview Practice", "📊 My Evaluation", "ℹ️ About Project"],
        label_visibility="collapsed",
    )

    st.markdown("#### Session controls")
    job_role = st.selectbox("Select role", ROLE_OPTIONS, key="job_role")
    st.file_uploader(
        "Upload resume",
        type=["pdf", "docx", "txt"],
        key=f"resume_upload_{st.session_state.resume_upload_version}",
        help="Optional. Resume files are not currently included in answer evaluation.",
    )
    st.caption("Resume upload is optional and is not currently used for scoring.")

    st.divider()
    st.metric("Completed evaluations", st.session_state.total_attempts)
    st.button(
        "↺  Reset interview",
        use_container_width=True,
        on_click=reset_interview,
    )
    st.caption("GPT-OSS · OpenRouter · LangGraph")


main_columns = st.columns([1, 2.45, 1], gap="medium")
with main_columns[1]:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">AI-powered interview preparation</div>
            <h1>PlacementSathi Feedback Assistant</h1>
            <p>Practice with role-specific questions, sharpen your answers, and get clear feedback to help you feel placement ready.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if page == "🏠 Interview Practice":
        st.markdown('<div class="eyebrow">Practice arena</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Build interview confidence</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-copy">A focused practice session for <strong>{job_role}</strong>. '
            "Choose a question, write your response, and get a thoughtful review.</div>",
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("#### 01 &nbsp; Choose your question")
            question_mode = st.radio(
                "Question source",
                ["✨ Generate with AI", "✍️ Enter manually"],
                horizontal=True,
                key="question_mode",
                label_visibility="collapsed",
            )

            if question_mode == "✨ Generate with AI":
                st.caption("Generate a fresh technical question tailored to your selected role.")
                if st.button(
                    "✦  Generate interview question",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        with st.spinner("Preparing a role-specific question..."):
                            generated = generate_interview_question(job_role)
                        st.session_state.generated_question_input = generated
                        st.session_state.generated_for_role = job_role
                        st.session_state.result = None
                    except Exception as error:
                        st.error(f"Question generation failed: {error}")

                if (
                    st.session_state.generated_for_role
                    and st.session_state.generated_for_role != job_role
                ):
                    st.warning("Your role changed. Generate a new question for this session.")

                question = st.text_area(
                    "Interview question",
                    key="generated_question_input",
                    height=100,
                    placeholder="Your generated question will appear here...",
                )
            else:
                question = st.text_area(
                    "Interview question",
                    key="custom_question",
                    height=100,
                    placeholder="Example: Explain the difference between a list and a tuple in Python.",
                )

        with st.container(border=True):
            st.markdown("#### 02 &nbsp; Shape your answer")
            student_answer = st.text_area(
                "Your answer",
                key="student_answer",
                height=190,
                placeholder=(
                    "Write your answer here. Explain your reasoning clearly "
                    "and include an example where possible."
                ),
            )
            st.caption(f"✎  {len(student_answer.split())} words")
            evaluate_button = st.button(
                "Evaluate my answer  →",
                type="primary",
                use_container_width=True,
            )

        if evaluate_button:
            if not question.strip():
                st.warning("Please generate or enter an interview question.")
            elif not student_answer.strip():
                st.warning("Please enter your interview answer.")
            else:
                initial_state = {
                    "job_role": job_role,
                    "question": question,
                    "student_answer": student_answer,
                    "analysis": "",
                    "score": 0,
                    "feedback": "",
                    "final_report": "",
                }
                try:
                    with st.spinner("Your answer is being reviewed..."):
                        result = workflow_app.invoke(initial_state)
                    st.session_state.result = result
                    st.session_state.total_attempts += 1
                except Exception as error:
                    st.error(f"Workflow execution failed: {error}")

        if st.session_state.result is not None:
            result = st.session_state.result
            score = result["score"]
            st.divider()
            st.markdown('<div class="eyebrow">Session debrief</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Your performance</div>', unsafe_allow_html=True)

            score_col, outcome_col, status_col = st.columns(3)
            with score_col:
                st.metric("Interview score", f"{score}/10")
            with outcome_col:
                st.metric("Performance", "Strong" if score >= 7 else "In progress")
            with status_col:
                st.metric("Evaluation", "Complete")

            st.progress(score / 10)
            if score >= 7:
                st.success("Strong response. You met the evaluation threshold.")
            else:
                st.info("A useful starting point. Review your coach's suggestions below.")

            st.markdown("#### Interview transcript")
            with st.chat_message("user", avatar="👤"):
                st.markdown("**Question**")
                st.write(result["question"])
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown("**Your answer**")
                st.write(result["student_answer"])
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(
                    f"**Coach review · {score}/10**  \n"
                    f"{'You are on the right track.' if score >= 7 else 'There is room to make this answer clearer and more complete.'}"
                )
                st.write(result["analysis"])

            analysis_tab, feedback_tab, report_tab = st.tabs(
                ["🔍 Answer analysis", "💡 Improvement feedback", "📄 Final report"]
            )
            with analysis_tab:
                st.markdown("#### What the evaluator noticed")
                st.write(result["analysis"])
                with st.expander("Review your submitted answer"):
                    st.write(result["student_answer"])
            with feedback_tab:
                st.markdown("#### Your next steps")
                if result.get("feedback"):
                    st.markdown(result["feedback"])
                else:
                    st.success("No additional improvement feedback was required.")
            with report_tab:
                st.markdown("#### Interview evaluation report")
                st.markdown(result["final_report"])
                st.download_button(
                    "Download evaluation report",
                    data=result["final_report"],
                    file_name="placement_feedback_report.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            st.caption(
                "AI-generated feedback is intended for interview practice and does not represent an official hiring decision."
            )

    elif page == "📊 My Evaluation":
        st.markdown('<div class="eyebrow">Your progress</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">My evaluation</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-copy">A snapshot of your most recent interview practice session.</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.result is None:
            st.info("No evaluation yet. Complete an interview practice session to see your results here.")
        else:
            result = st.session_state.result
            score_col, count_col = st.columns(2)
            with score_col:
                st.metric("Latest score", f"{result['score']}/10")
            with count_col:
                st.metric("Completed evaluations", st.session_state.total_attempts)

            with st.container(border=True):
                st.markdown("#### Latest interview")
                st.markdown(f"**Role**  \n{result['job_role']}")
                st.markdown(f"**Question**  \n{result['question']}")
                st.markdown(f"**Score**  \n{result['score']}/10")
                st.markdown("#### Coach feedback")
                if result.get("feedback"):
                    st.markdown(result["feedback"])
                else:
                    st.success("No additional improvement feedback was required.")
                st.download_button(
                    "Download latest report",
                    data=result["final_report"],
                    file_name="placement_feedback_report.txt",
                    mime="text/plain",
                )

    elif page == "ℹ️ About Project":
        st.markdown('<div class="eyebrow">Behind the assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">About PlacementSathi</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-copy">An AI-powered interview practice space that evaluates student answers and offers personalized feedback.</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("#### Technology stack")
            stack_col, tools_col = st.columns(2)
            with stack_col:
                st.markdown(
                    "- **Python** — application runtime\n"
                    "- **LangChain** — model integration\n"
                    "- **LangGraph** — workflow orchestration\n"
                    "- **OpenRouter** — AI model access"
                )
            with tools_col:
                st.markdown(
                    "- **Streamlit** — interactive interface\n"
                    "- **LangSmith** — workflow tracing\n"
                    "- **GPT-OSS** — language model"
                )

        with st.container(border=True):
            st.markdown("#### Evaluation workflow")
            st.code(
                "Analyze answer → Evaluate score → "
                "Generate feedback when needed → Create final report",
                language="text",
            )

    st.markdown(
        """
        <div class="footer">
            PlacementSathi &nbsp;·&nbsp; Built with LangChain, LangGraph, Streamlit and LangSmith
            <br>AI-powered interview preparation for students
        </div>
        """,
        unsafe_allow_html=True,
    )
