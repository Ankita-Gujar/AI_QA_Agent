from pathlib import Path
import streamlit as st

from modules.pdf_reader import read_pdf
from modules.document_object import build_document_object
#from modules.page_renderer import render_page
from modules.object_matcher import ObjectMatcher
from modules.difference_builder import DifferenceBuilder
from modules.prompt_builder import PromptBuilder
from modules.ai_agent import AIAgent



# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI DTP QA Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# Load CSS
# ---------------------------------------------------

css_file = Path(__file__).parent / "assets" / "style.css"

if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">AI DTP QA Agent</div>
        <div class="app-subtitle">
            AI Powered Document Layout & Quality Analysis
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------------------
# Languages
# ---------------------------------------------------

languages = [
    "English",
    "Marathi",
    "Hindi",
    "Gujarati",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Punjabi",
    "Bengali",
    "Japanese",
    "Chinese",
    "Korean",
    "German",
    "French",
    "Spanish",
    "Italian",
    "Portuguese"
]

# ---------------------------------------------------
# Upload Section
# ---------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("📄 Source PDF")

    source_pdf = st.file_uploader(
        "Upload Source PDF",
        type=["pdf"],
        key="source"
    )

    source_language = st.selectbox(
        "Source Language",
        languages,
        index=0
    )

with right:

    st.subheader("🌍 Target PDF")

    target_pdf = st.file_uploader(
        "Upload Target PDF",
        type=["pdf"],
        key="target"
    )

    target_language = st.selectbox(
        "Target Language",
        languages,
        index=10
    )

st.divider()

# ---------------------------------------------------
# Compare Button
# ---------------------------------------------------

compare = st.button(
    "🚀 Start AI QA",
    use_container_width=True
)

# ---------------------------------------------------
# Compare
# ---------------------------------------------------

if compare:

    if source_pdf is None or target_pdf is None:

        st.error("Please upload both PDF files.")

    else:

        import os

        # Create folders
        os.makedirs("uploads/source", exist_ok=True)
        os.makedirs("uploads/target", exist_ok=True)

        # Save PDFs
        source_path = "uploads/source/source.pdf"
        target_path = "uploads/target/target.pdf"

        with open(source_path, "wb") as f:
            f.write(source_pdf.getbuffer())

        with open(target_path, "wb") as f:
            f.write(target_pdf.getbuffer())

        # Progress
        progress = st.progress(0)
        status = st.empty()

        progress = st.progress(0)
        status = st.empty()

        def update_progress(percent, message):
            progress.progress(percent)
            status.info(message)

        # Read PDFs
        update_progress(10, "📖 Reading Source PDF...")
        source_data = read_pdf(source_path)
        update_progress(20, "📖 Reading Target PDF...")
        target_data = read_pdf(target_path)

        # Build Document Object Model (DOM)
        update_progress(30, "📑 Building Source Document Model...")
        source_dom = build_document_object(source_data)
        update_progress(40, "📑 Building Target Document Model...")
        target_dom = build_document_object(target_data)


        # -----------------------------------------
        # Object Matching
        # -----------------------------------------
        update_progress(50, "🔍 Comparing paragraphs, images and tables...")
        matcher = ObjectMatcher()

        matches = matcher.compare(
            source_dom,
            target_dom
        )

        # -----------------------------------------
        # Build Differences
        # -----------------------------------------
        update_progress(60, "📊 Detecting layout differences...")
        builder = DifferenceBuilder()
        differences = builder.build(matches)

        # -----------------------------------------
       
        # -----------------------------------------
        # Build AI Prompt
        # -----------------------------------------
        update_progress(70, "📝 Preparing AI prompt...")
        prompt_builder = PromptBuilder(
            source_language,
            target_language
        )

        prompt = prompt_builder.build(differences)

        # -----------------------------------------
        # AI Analysis
        # -----------------------------------------
        update_progress(80, "🤖 AI is reviewing the document...")
        agent = AIAgent()
        with st.spinner("🧠 AI is analyzing the document. Please wait..."):
            ai_report = agent.analyze(prompt)
        os.makedirs("reports", exist_ok=True)

        update_progress(95, "💾 Saving QA report...")
        with open(
            "reports/AI_DTP_QA_Report.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(ai_report)

        progress.progress(100)
        status.success("✅ QA Analysis Completed")

        st.success("🎉 AI QA Completed Successfully")

        # -----------------------------------------
        # Display AI Report
        # -----------------------------------------

        st.divider()

        st.header("🤖 AI QA Report")

        st.text_area(
            "AI QA Report",
            ai_report,
            height=700
        )
        

    with open(
        "reports/AI_DTP_QA_Report.txt",
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download QA Report",
            data=file,
            file_name="AI_DTP_QA_Report.txt",
            mime="text/plain"
        )