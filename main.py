import textwrap
import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# =========================================================
# HELPER: render HTML safely (no code-block bugs)
# =========================================================

def html(markup: str):
    """Render raw HTML in Streamlit without markdown indentation issues."""
    st.markdown(textwrap.dedent(markup).strip(), unsafe_allow_html=True)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PostCraft AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* =========================================================
   GLOBAL
   ========================================================= */

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 5%, rgba(124, 58, 237, 0.16), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(37, 99, 235, 0.13), transparent 30%),
        #080b14;
    color: #f8fafc;
}

.main .block-container {
    max-width: 1150px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #0b0f1a;
    border-right: 1px solid rgba(255,255,255,0.07);
}

section[data-testid="stSidebar"] > div {
    padding: 1.4rem 1.15rem;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 10px;
}

.sidebar-logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    box-shadow: 0 8px 25px rgba(124,58,237,0.28);
    font-size: 20px;
}

.sidebar-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 800;
}

.sidebar-subtitle {
    color: #64748b;
    font-size: 10px;
    margin-top: 2px;
}

.sidebar-heading {
    color: #e2e8f0;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 8px;
}

.sidebar-feature {
    color: #94a3b8;
    font-size: 12px;
    padding: 6px 0;
}

.workflow {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 12px;
    color: #94a3b8;
    font-size: 11px;
    line-height: 1.8;
}

.workflow .arrow {
    text-align: center;
    color: #8b5cf6;
}

.tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.tech-stack span {
    padding: 6px 9px;
    border-radius: 7px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    color: #94a3b8;
    font-size: 10px;
}

.sidebar-footer {
    text-align: center;
    color: #475569;
    font-size: 9px;
    line-height: 1.6;
    margin-top: 28px;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    text-align: center;
    padding: 35px 10px 38px;
}

.hero-image {
    width: 110px;
    height: 110px;
    object-fit: contain;
    margin-bottom: 18px;
    filter: drop-shadow(0 15px 35px rgba(124,58,237,0.30));
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: rgba(124,58,237,0.10);
    border: 1px solid rgba(124,58,237,0.22);
    color: #c4b5fd;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    margin-bottom: 17px;
}

.hero h1 {
    margin: 0;
    font-size: 52px;
    line-height: 1.08;
    letter-spacing: -2px;
    font-weight: 800;
    color: #ffffff;
}

.gradient {
    background: linear-gradient(90deg, #a78bfa, #818cf8, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 620px;
    margin: 17px auto 0;
    color: #94a3b8;
    font-size: 15px;
    line-height: 1.7;
}


/* =========================================================
   GENERATOR CARD
   ========================================================= */

.generator-card {
    background: linear-gradient(145deg, rgba(17,24,39,0.90), rgba(15,23,42,0.70));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 27px;
    box-shadow: 0 25px 70px rgba(0,0,0,0.25);
}

.card-heading {
    display: flex;
    align-items: center;
    gap: 11px;
}

.card-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(124,58,237,0.13);
    border: 1px solid rgba(124,58,237,0.20);
}

.card-title {
    color: #ffffff;
    font-size: 19px;
    font-weight: 700;
}

.card-description {
    margin-left: 51px;
    margin-top: 4px;
    margin-bottom: 23px;
    color: #64748b;
    font-size: 12px;
}


/* =========================================================
   INPUTS
   ========================================================= */

label {
    color: #cbd5e1 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] > div {
    background: #111827 !important;
    border: 1px solid #263244 !important;
    border-radius: 11px !important;
    min-height: 47px;
}

div[data-baseweb="select"] span {
    color: #e2e8f0 !important;
}


/* =========================================================
   GENERATE BUTTON
   ========================================================= */

.stButton {
    margin-top: 23px;
}

.stButton > button {
    width: 100%;
    height: 51px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg, #7c3aed, #6366f1, #2563eb);
    color: #ffffff;
    font-size: 14px;
    font-weight: 700;
    box-shadow: 0 10px 28px rgba(99,102,241,0.25);
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 35px rgba(99,102,241,0.35);
}


/* =========================================================
   OUTPUT HEADER
   ========================================================= */

.output-title {
    margin-top: 42px;
    margin-bottom: 17px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.output-heading {
    color: #ffffff;
    font-size: 20px;
    font-weight: 700;
}

.output-subtitle {
    color: #64748b;
    font-size: 11px;
}


/* =========================================================
   LINKEDIN PREVIEW
   ========================================================= */

.linkedin-card {
    background: #ffffff;
    color: #172033;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.30);
}

.profile {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 18px;
}

.avatar {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: #ffffff;
    font-weight: 800;
}

.profile-name {
    color: #172033;
    font-size: 13px;
    font-weight: 700;
}

.profile-role {
    color: #64748b;
    font-size: 10px;
    margin-top: 2px;
}

.ai-tag {
    margin-left: auto;
    padding: 5px 8px;
    border-radius: 6px;
    background: #f3e8ff;
    color: #7c3aed;
    font-size: 9px;
    font-weight: 700;
}

.post-content {
    color: #334155;
    font-size: 14px;
    line-height: 1.75;
    white-space: pre-wrap;
}

.post-divider {
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0 12px;
}

.post-stats {
    display: flex;
    justify-content: space-between;
    color: #64748b;
    font-size: 10px;
}


/* =========================================================
   COPY BOX
   ========================================================= */

.copy-label {
    color: #cbd5e1;
    font-size: 12px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 7px;
}

textarea {
    background: #0f172a !important;
    color: #e2e8f0 !important;
    border: 1px solid #263244 !important;
    border-radius: 11px !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    padding-top: 45px;
    color: #475569;
    font-size: 10px;
    line-height: 1.8;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {
    .hero h1 {
        font-size: 38px;
        letter-spacing: -1px;
    }
    .hero-image {
        width: 85px;
        height: 85px;
    }
    .generator-card {
        padding: 20px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    html("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">✨</div>
        <div>
            <div class="sidebar-title">PostCraft AI</div>
            <div class="sidebar-subtitle">GenAI Content Studio</div>
        </div>
    </div>
    """)

    st.divider()

    html('<div class="sidebar-heading">⚡ Features</div>')

    html("""
    <div class="sidebar-feature">✓ Few-Shot Learning</div>
    <div class="sidebar-feature">✓ Multi-Language</div>
    <div class="sidebar-feature">✓ LinkedIn Optimized</div>
    <div class="sidebar-feature">✓ Fast Generation</div>
    """)

    st.divider()

    html('<div class="sidebar-heading">🧠 How it works</div>')

    html("""
    <div class="workflow">
        <div>🎯 Select Topic</div>
        <div class="arrow">↓</div>
        <div>🧩 Build Prompt</div>
        <div class="arrow">↓</div>
        <div>🤖 Groq LLM</div>
        <div class="arrow">↓</div>
        <div>📝 LinkedIn Post</div>
    </div>
    """)

    st.divider()

    html('<div class="sidebar-heading">🛠 Technology</div>')

    html("""
    <div class="tech-stack">
        <span>Python</span>
        <span>Streamlit</span>
        <span>LangChain</span>
        <span>Groq</span>
    </div>
    """)

    html("""
    <div class="sidebar-footer">
        PostCraft AI<br>
        Generative AI LinkedIn Post Generator
    </div>
    """)


# =========================
# HERO SECTION
# =========================

html("""
<h1 style='text-align:center;'>
    Turn ideas into <span style='color:#7c3aed;'>impactful posts.</span>
</h1>
""")

html("""
<p style='text-align:center; color:#6b7280; font-size:17px;'>
    Create engaging LinkedIn content in seconds.<br>
    Choose your topic, length and language — let AI handle the writing.
</p>
""")

st.markdown("---")


# =========================================================
# LOAD FEW SHOT DATA
# =========================================================

fs = FewShotPosts()
tags = fs.get_tags()


# =========================
# CREATE POST CARD
# =========================

st.subheader("✍️ Create your post")

st.caption(
    "Customize your content and generate an AI-powered LinkedIn post."
)


# =========================================================
# INPUT CONTROLS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    selected_tag = st.selectbox("🎯 Topic", options=tags)

with col2:
    selected_length = st.selectbox(
        "📏 Length",
        options=["Short", "Medium", "Long"]
    )

with col3:
    selected_language = st.selectbox(
        "🌐 Language",
        options=["English", "Hinglish"]
    )


# =========================================================
# GENERATE
# =========================================================

generate = st.button("✨  Generate LinkedIn Post")


if generate:
    with st.spinner("✨ AI is crafting your post..."):
        try:
            post = generate_post(
                selected_length,
                selected_language,
                selected_tag
            )
            st.session_state["generated_post"] = post
        except Exception as e:
            st.error(f"Something went wrong: {e}")


# =========================================================
# OUTPUT
# =========================================================

if "generated_post" in st.session_state:

    post = st.session_state["generated_post"]
    character_count = len(post)

    html("""
    <div class="output-title">
        <div class="output-heading">📝 Generated Post</div>
        <div class="output-subtitle">AI-generated content</div>
    </div>
    """)

        # -----------------------------------------------------
    # LINKEDIN PREVIEW
    # -----------------------------------------------------

    linkedin_html = (
        '<div class="linkedin-card">'
        '<div class="profile">'
        '<div class="avatar">K</div>'
        '<div>'
        '<div class="profile-name">Kushlesh Mishra</div>'
        '<div class="profile-role">Data Science • AI/ML • Generative AI</div>'
        '</div>'
        '<div class="ai-tag">AI GENERATED</div>'
        '</div>'
        '<div class="post-content">'
        f'{post}'
        '</div>'
        '<div class="post-divider"></div>'
        '<div class="post-stats">'
        '<span>👍 Like</span>'
        '<span>💬 Comment</span>'
        '<span>↗ Repost</span>'
        '<span>↗ Send</span>'
        '</div>'
        '</div>'
    )

    st.markdown(linkedin_html, unsafe_allow_html=True)

    # -----------------------------------------------------
    # COPY AREA
    # -----------------------------------------------------

    html('<div class="copy-label">📋 Copy your post</div>')

    st.text_area(
        "Copy",
        value=post,
        height=200,
        label_visibility="collapsed"
    )

    st.caption(
        f"{selected_tag}  •  "
        f"{selected_length}  •  "
        f"{selected_language}  •  "
        f"{character_count} characters"
    )


# =========================================================
# FOOTER
# =========================================================

html("""
<div class="footer">
    PostCraft AI · Generative AI LinkedIn Post Generator
    <br>
    Built with Python · Streamlit · LangChain · Groq
</div>
""")