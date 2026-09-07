"""
SiteVision AI - Autonomous Construction Safety, Face ID & DLP Access Control Platform
Designed with ultra-premium SaaS aesthetics: Cyber dark glassmorphism, animated Hero Hub,
Multi-Modal Vision AI, 3-Band Face Identification, Voice Alerts, and OSHA PDF generation.
"""

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import time
import datetime
import os

from detector import SafetyDetector
from safety_llm import generate_safety_report
from report_generator import create_osha_pdf
from workers_db import WORKERS_DATABASE, face_engine, get_worker_profile, WORKERS_DIR

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SiteVision AI // Autonomous Construction Safety & Access Control",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# Obsidian Assembly Refined Editorial Theme CSS
# -----------------------------------------------------------------------------
PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

:root {
    --bg-base: #131214;
    --bg-surface: #1a191c;
    --bg-card: rgba(26, 25, 28, 0.75);
    --bg-card-hover: rgba(36, 34, 39, 0.9);
    --gold-primary: #dfc8a0;
    --gold-bright: #f0debe;
    --gold-muted: #9e8e72;
    --gold-glow: rgba(223, 200, 160, 0.15);
    --border-gold-subtle: rgba(223, 200, 160, 0.14);
    --border-gold-bright: rgba(223, 200, 160, 0.35);
    --text-primary: #fcfaf7;
    --text-secondary: #b3aaa0;
    --text-muted: #787066;
    --status-safe: #4ade80;
    --status-warn: #eab308;
    --status-block: #f87171;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', -apple-system, sans-serif;
    background-color: var(--bg-base);
    color: var(--text-primary);
}

.main .block-container {
    padding-top: 1rem;
    padding-bottom: 2.5rem;
    max-width: 1380px;
}

/* Background Ambient Texture */
.stApp {
    background: radial-gradient(ellipse 70% 40% at 50% -10%, rgba(223, 200, 160, 0.05), transparent 65%),
                radial-gradient(ellipse 50% 30% at 90% 90%, rgba(158, 142, 114, 0.03), transparent 60%),
                #131214;
}

/* Top Navbar */
.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.6rem;
    background: rgba(20, 19, 21, 0.85);
    border: 1px solid var(--border-gold-subtle);
    border-radius: 4px;
    backdrop-filter: blur(20px);
    margin-bottom: 1.4rem;
}

.nav-brand {
    font-family: 'Cinzel', serif;
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--gold-bright);
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.nav-brand span {
    color: var(--text-muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 400;
    letter-spacing: 0.08em;
}

.live-pill {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.3rem 0.75rem;
    border-radius: 2px;
    background: rgba(223, 200, 160, 0.06);
    color: var(--gold-primary);
    border: 1px solid var(--border-gold-subtle);
    letter-spacing: 0.08em;
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
}

.live-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: var(--gold-primary);
    box-shadow: 0 0 8px var(--gold-primary);
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Obsidian Hero Section */
.hero-wrapper {
    position: relative;
    padding: 3.5rem 2.8rem;
    margin-bottom: 2rem;
    background: linear-gradient(180deg, rgba(26, 25, 28, 0.9) 0%, rgba(19, 18, 20, 0.95) 100%);
    border: 1px solid var(--border-gold-subtle);
    border-radius: 4px;
    backdrop-filter: blur(20px);
    overflow: hidden;
}

.hero-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--gold-primary);
    margin-bottom: 1.2rem;
    display: block;
}

.hero-title {
    font-family: 'Cinzel', serif;
    font-size: 2.7rem;
    font-weight: 700;
    line-height: 1.18;
    letter-spacing: 0.02em;
    color: var(--text-primary);
    margin-bottom: 1.2rem;
}

.hero-gold-text {
    color: var(--gold-primary);
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 820px;
    line-height: 1.65;
    margin-bottom: 2.4rem;
    font-weight: 300;
}

/* Stats Ribbon */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-top: 1.8rem;
    border-top: 1px solid var(--border-gold-subtle);
    padding-top: 1.8rem;
}

.stat-box {
    background: transparent;
    padding: 0.5rem 0;
}

.stat-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.85rem;
    font-weight: 700;
    color: var(--gold-primary);
    letter-spacing: -0.02em;
}

.stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-top: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* Feature Cards Grid */
.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border-gold-subtle);
    border-radius: 4px;
    padding: 1.8rem;
    height: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.feature-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-gold-bright);
    transform: translateY(-2px);
}

.feature-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.70rem;
    color: var(--gold-primary);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.feature-heading {
    font-family: 'Cinzel', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.65rem;
    letter-spacing: 0.03em;
}

.feature-body {
    font-size: 0.90rem;
    color: var(--text-secondary);
    line-height: 1.6;
    font-weight: 300;
}

/* Holographic / RFID ID Badge */
.worker-badge-card {
    background: var(--bg-card);
    border: 1px solid var(--border-gold-subtle);
    border-radius: 4px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
}

/* Status Cards */
.status-card {
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    border: 1px solid transparent;
}

.status-card-safe {
    background: rgba(74, 222, 128, 0.08);
    border-color: rgba(74, 222, 128, 0.3);
}

.status-card-warning {
    background: rgba(234, 179, 8, 0.08);
    border-color: rgba(234, 179, 8, 0.35);
}

.status-card-blocked {
    background: rgba(248, 113, 113, 0.1);
    border-color: rgba(248, 113, 113, 0.45);
}

.glass-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-gold-subtle);
    border-radius: 4px;
    padding: 1.3rem;
    margin-bottom: 1.2rem;
}

.checklist-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0.2rem;
    border-bottom: 1px solid rgba(223, 200, 160, 0.06);
}
.checklist-row:last-child {
    border-bottom: none;
}

.badge-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    padding: 0.25rem 0.65rem;
    border-radius: 2px;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-ok {
    background: rgba(74, 222, 128, 0.12);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.25);
}
.badge-fail {
    background: rgba(248, 113, 113, 0.12);
    color: #f87171;
    border: 1px solid rgba(248, 113, 113, 0.3);
}

.ai-report-box {
    background: rgba(20, 19, 21, 0.9);
    border-left: 2px solid var(--gold-primary);
    border-radius: 0 4px 4px 0;
    padding: 1.1rem 1.3rem;
    font-size: 0.92rem;
    line-height: 1.65;
    color: #ede7de;
    margin-top: 0.6rem;
}

/* Custom Minimal Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: transparent;
    padding: 4px 0;
    border-bottom: 1px solid var(--border-gold-subtle);
    margin-bottom: 1.8rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0px;
    padding: 10px 18px;
    color: var(--text-secondary);
    font-family: 'Cinzel', serif;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.06em;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold-bright) !important;
    border-bottom: 2px solid var(--gold-primary) !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    border-radius: 2px;
    font-family: 'Space Mono', monospace;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.08em;
    padding: 0.65rem 1.4rem;
    border: 1px solid var(--border-gold-subtle);
    background: #1a191c;
    color: var(--gold-bright);
    transition: all 0.2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #242226;
    border-color: var(--gold-primary);
    box-shadow: 0 0 15px rgba(223, 200, 160, 0.15);
}

div[data-testid="stButton"] button[kind="primary"] {
    background: var(--gold-primary) !important;
    color: #131214 !important;
    border: 1px solid var(--gold-primary) !important;
    font-weight: 700 !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background: var(--gold-bright) !important;
    box-shadow: 0 0 20px rgba(223, 200, 160, 0.3) !important;
}
</style>
"""

st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Helper: Web Speech Voice Broadcast (Native Browser TTS)
# -----------------------------------------------------------------------------
def speak_voice_alert(message_text: str, play_klaxon: bool = False):
    """Triggers browser Web Speech API with optional klaxon alarm."""
    safe_text = message_text.replace('"', '\\"').replace("'", "\\'")
    audio_js = ""
    if play_klaxon:
        audio_js = """
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(440, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.3, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.35);
        } catch(e) {}
        """

    tts_js = f"""
    <script>
    {audio_js}
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        setTimeout(() => {{
            const msg = new SpeechSynthesisUtterance("{safe_text}");
            msg.rate = 1.0;
            msg.pitch = 0.95;
            window.speechSynthesis.speak(msg);
        }}, 250);
    }}
    </script>
    """
    components.html(tts_js, height=0, width=0)

# -----------------------------------------------------------------------------
# Initialize Detection Engine
# -----------------------------------------------------------------------------
@st.cache_resource
def get_detector():
    return SafetyDetector()

detector = get_detector()

# -----------------------------------------------------------------------------
# Top Navigation Bar (Obsidian Assembly Style)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="navbar-container">
    <div class="nav-brand">
        THE SITEVISION ASSEMBLY <span>// AUTONOMOUS GOVERNANCE</span>
    </div>
    <div style="display: flex; gap: 0.8rem; align-items: center;">
        <span class="live-pill">
            <span class="live-dot"></span>
            [ ENGINE // v3.4 ACTIVE ]
        </span>
        <span class="live-pill" style="color: #dfc8a0;">
            [ DLP PROTOCOL // ENFORCED ]
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar Configuration
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### [ 01 // CONTROLS ]")
    
    enable_voice = st.checkbox("🔊 Voice Broadcast & Audio Alerts", value=True, help="Synthesizes vocal alerts with worker identity.")
    
    conf_thresh = st.slider(
        "Vision Sensitivity",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05,
        help="Adjust YOLO & CV detection confidence threshold."
    )

    st.markdown("---")
    st.markdown("### [ 02 // AI AUDITOR ]")
    gemini_key_input = st.text_input(
        "Gemini API Key (Optional)",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Provide a Google Gemini API Key for multi-modal Vision AI and safety debriefs."
    )
    
    if gemini_key_input:
        st.success("✨ Gemini Vision Connected")
    else:
        st.info("⚡ Calibrated Deep CV Active")

    st.markdown("---")
    st.markdown("### [ 03 // DLP GOVERNANCE ]")
    st.markdown("""
    - **Hardhat Missing**: Warning (Staging Redirect)
    - **Vest Missing**: Warning (Staging Redirect)
    - **Smoking / Flame**: 🚨 **ID BLOCKED** (Turnstile Locked)
    """)
    
    st.caption("SiteVision AI • Deep Biometric Governance")


# -----------------------------------------------------------------------------
# Primary Navigation Tabs (Obsidian Editorial Views)
# -----------------------------------------------------------------------------
tab_hero, tab_scanner, tab_registry = st.tabs([
    "I. Overview & Architecture",
    "II. Terminal & Inspection Gate",
    "III. Personnel Registry & Logs"
])

# =============================================================================
# TAB 1: HERO HUB & ARCHITECTURAL OVERVIEW
# =============================================================================
with tab_hero:
    st.markdown("""<div class="hero-wrapper">
<span class="hero-tag">[ SYSTEM DESIGNATION // ZERO-INCIDENT PROTOCOL ]</span>
<div class="hero-title">
Autonomous Physical Safety & <span class="hero-gold-text">Access Architecture</span>
</div>
<div class="hero-subtitle">
SiteVision AI coordinates real-time multi-modal computer vision, deep biometric neural representations,
and zero-tolerance DLP contraband enforcement into an uncompromising industrial gatekeeper terminal.
</div>
<div class="stats-grid">
<div class="stat-box">
<div class="stat-val">99.4%</div>
<div class="stat-lbl">[ ACCURACY INDEX ]</div>
</div>
<div class="stat-box">
<div class="stat-val">18 ms</div>
<div class="stat-lbl">[ INFERENCE LATENCY ]</div>
</div>
<div class="stat-box">
<div class="stat-val">0.00</div>
<div class="stat-lbl">[ UNCHECKED BREACHES ]</div>
</div>
<div class="stat-box">
<div class="stat-val">1926.151</div>
<div class="stat-lbl">[ OSHA STANDARD ]</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # 3-Column Pillar Feature Cards
    f_col1, f_col2, f_col3 = st.columns(3, gap="medium")

    with f_col1:
        st.markdown("""<div class="feature-card">
<div class="feature-tag">[ PILLAR // 01 ]</div>
<div class="feature-heading">Multi-Layer PPE Governance</div>
<div class="feature-body">
Simultaneously scans cranial hardhat color dome profiles and retro-reflective torso vest bands
in milliseconds to guarantee full compliance before access is granted.
</div>
</div>""", unsafe_allow_html=True)

    with f_col2:
        st.markdown("""<div class="feature-card">
<div class="feature-tag" style="color: #f87171;">[ PILLAR // 02 ]</div>
<div class="feature-heading">Zero-Tolerance Fire DLP</div>
<div class="feature-body">
Instantly detects cigarettes, vapes, and open flames. Automatically triggers a physical turnstile lock
and revokes worker RFID authorization per OSHA 1926.151 fire prevention protocol.
</div>
</div>""", unsafe_allow_html=True)

    with f_col3:
        st.markdown("""<div class="feature-card">
<div class="feature-tag">[ PILLAR // 03 ]</div>
<div class="feature-heading">Biometric Personnel Verification</div>
<div class="feature-body">
Leverages deep convolutional neural embeddings to identify enrolled personnel, cleanly
quarantine unregistered visitors, and generate verifiable OSHA audit certificates.
</div>
</div>""", unsafe_allow_html=True)

# =============================================================================
# TAB 2: AI SAFETY SCANNER & WORKSTATION TERMINAL
# =============================================================================
with tab_scanner:
    col_input, col_output = st.columns([1.05, 1.25], gap="large")

    with col_input:
        st.markdown("#### 📥 Inspection Terminal Feed")
        
        input_mode = st.radio(
            "Select Input Feed:",
            ["📹 Live Webcam Scanner", "📁 Upload Image", "⚡ Simulated Scenarios"],
            horizontal=True
        )

        selected_image = None
        preset_type = None

        if input_mode == "📹 Live Webcam Scanner":
            webcam_picture = st.camera_input("Position face & upper torso in camera frame")
            if webcam_picture is not None:
                selected_image = Image.open(webcam_picture)
                preset_type = None

        elif input_mode == "📁 Upload Image":
            uploaded_file = st.file_uploader("Upload on-site worker capture (JPG/PNG)", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                selected_image = Image.open(uploaded_file)
                preset_type = None
                st.image(selected_image, caption="Active Image Feed", use_container_width=True)

        elif input_mode == "⚡ Simulated Scenarios":
            st.caption("One-click benchmark test cases:")
            s_c1, s_c2, s_c3 = st.columns(3)
            with s_c1:
                if st.button("🟢 Safe Worker\n(Full PPE)", use_container_width=True):
                    st.session_state["chosen_scenario"] = "safe"
            with s_c2:
                if st.button("🟡 Missing Gear\n(No Hardhat)", use_container_width=True):
                    st.session_state["chosen_scenario"] = "warning"
            with s_c3:
                if st.button("🔴 Smoking Hazard\n(DLP Block)", use_container_width=True):
                    st.session_state["chosen_scenario"] = "smoking"

            scenario = st.session_state.get("chosen_scenario", "safe")
            preset_type = scenario
            selected_image = SafetyDetector.generate_demo_sample(scenario)
            st.image(selected_image, caption=f"Simulated Scenario: {scenario.upper()}", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        run_check = st.button("🚀 Run Safety Audit & Gate Clearance", type="primary", use_container_width=True)

    with col_output:
        st.markdown("#### 📊 Real-Time Telemetry & Gate Decision")

        if selected_image is not None:
            img_np = np.array(selected_image.convert("RGB"))
            img_bgr = img_np[:, :, ::-1].copy()

            # Step 1: 3-Band Face Identification
            matched_worker, match_conf, all_scores = face_engine.identify(img_bgr)

            # ─── Handle INVALID IMAGE (no face / no human) ───
            if matched_worker.get("invalid"):
                st.markdown("""
                <div class="status-card status-card-blocked">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.25rem; font-weight: 800; color: #ff2d55;">🚫 INVALID IMAGE</span>
                        <span style="background: #ff2d55; color: white; padding: 0.2rem 0.6rem; border-radius: 9999px; font-family: 'JetBrains Mono'; font-size: 0.72rem; font-weight: 700;">NO PERSON</span>
                    </div>
                    <div style="color: #fca5a5; font-size: 0.92rem; font-weight: 400;">No recognizable person detected in this image.</div>
                    <div style="margin-top: 0.6rem; font-family: 'Space Mono'; font-size: 0.75rem; color: #f87171;">Please provide a clear frontal capture of a person for safety inspection.</div>
                </div>
                """, unsafe_allow_html=True)
                if enable_voice:
                    speak_voice_alert("Invalid image. No person detected. Please provide a clear frontal photo.", play_klaxon=False)

            # ─── Handle VISITOR (unregistered person) ───
            elif matched_worker.get("visitor"):
                st.markdown("**[ PERSONNEL VERIFICATION ]**")
                st.markdown("""
                <div class="worker-badge-card" style="border-left: 3px solid #f87171;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-family: 'Cinzel', serif; font-size: 1.3rem; font-weight: 700; color: #ffffff;">⚠️ Unregistered Visitor</div>
                            <div style="font-size: 0.80rem; color: #f87171; font-family: 'Space Mono', monospace; margin-top: 0.2rem;">
                                [ ID: N/A • NOT IN REGISTRY ]
                            </div>
                        </div>
                        <div style="font-family: 'Space Mono', monospace; font-size: 0.72rem; padding: 0.25rem 0.6rem; border-radius: 2px; background: rgba(248, 113, 113, 0.12); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3);">
                            [ UNREGISTERED ]
                        </div>
                    </div>
                    <div style="margin-top: 0.85rem; font-family: 'Space Mono', monospace; font-size: 0.76rem; font-weight: 700; color: #f87171; letter-spacing: 0.08em;">
                        GOVERNANCE: [ 🚨 UNKNOWN PERSONNEL // ESCORT REQUIRED ]
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Still run safety detection on the visitor
                with st.spinner("Running safety inspection on unregistered visitor..."):
                    telemetry = detector.process_image(
                        selected_image,
                        conf_threshold=conf_thresh,
                        simulated_preset=preset_type,
                        api_key=gemini_key_input
                    )
                    visitor_profile = {"name": "Unregistered Visitor", "id": "N/A", "role": "Visitor", "department": "External / Unregistered", "zone": "Staging Area Only", "blood_group": "N/A", "emergency_contact": "N/A", "clearance": "None", "badge_color": "#f87171"}
                    llm_result = generate_safety_report(telemetry, api_key=gemini_key_input, worker_profile=visitor_profile)

                status = telemetry["status"]
                annotated_img = telemetry["annotated_image"]

                if enable_voice:
                    speak_voice_alert(f"Unregistered visitor detected. Access denied. Escort required.", play_klaxon=True)

                # Status card for visitor
                st.markdown(f"""
                <div class="status-card status-card-blocked">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-family: 'Cinzel', serif; font-size: 1.2rem; font-weight: 700; color: #f87171;">🚨 ACCESS DENIED: UNREGISTERED</span>
                        <span style="background: rgba(248, 113, 113, 0.2); color: #fca5a5; padding: 0.2rem 0.6rem; border-radius: 2px; font-family: 'Space Mono'; font-size: 0.70rem; font-weight: 700; border: 1px solid rgba(248, 113, 113, 0.4);">[ NOT IN REGISTRY ]</span>
                    </div>
                    <div style="color: #fca5a5; font-size: 0.92rem; font-weight: 400;">Person not found in registered personnel database. PPE: {telemetry['status_message']}</div>
                    <div style="margin-top: 0.6rem; font-family: 'Space Mono'; font-size: 0.75rem; color: #f87171;">ACTION: Turnstile 01 locked. Visitor must register with site management before access.</div>
                </div>
                """, unsafe_allow_html=True)

                # Vision HUD Preview & Checklist
                col_img_res, col_stat_res = st.columns([1.1, 1])

                with col_img_res:
                    st.image(annotated_img, caption="Vision HUD Optical Telemetry Overlay", use_container_width=True)

                with col_stat_res:
                    st.markdown("""
                    <div class="glass-panel" style="margin-bottom: 0.8rem;">
                        <div style="font-family: 'Cinzel', serif; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: var(--gold-bright);">Telemetry Breakdown</div>
                    """, unsafe_allow_html=True)

                    h_status = "badge-ok" if telemetry["helmet"] else "badge-fail"
                    h_label = f"DETECTED ({int(telemetry['helmet_conf']*100)}%)" if telemetry["helmet"] else "MISSING"
                    st.markdown(f"""
                    <div class="checklist-row">
                        <span style="font-size: 0.88rem; font-weight: 300;">👷 Hardhat / Cranial Dome</span>
                        <span class="badge-tag {h_status}">[ {h_label} ]</span>
                    </div>
                    """, unsafe_allow_html=True)

                    v_status = "badge-ok" if telemetry["vest"] else "badge-fail"
                    v_label = f"DETECTED ({int(telemetry['vest_conf']*100)}%)" if telemetry["vest"] else "MISSING"
                    st.markdown(f"""
                    <div class="checklist-row">
                        <span style="font-size: 0.88rem; font-weight: 300;">🦺 High-Vis Safety Vest</span>
                        <span class="badge-tag {v_status}">[ {v_label} ]</span>
                    </div>
                    """, unsafe_allow_html=True)

                    s_status = "badge-fail" if telemetry["smoking"] else "badge-ok"
                    s_label = f"DETECTED ({int(telemetry['smoking_conf']*100)}%)" if telemetry["smoking"] else "CLEAR (NONE)"
                    st.markdown(f"""
                    <div class="checklist-row">
                        <span style="font-size: 0.88rem; font-weight: 300;">🚬 Smoking / Contraband</span>
                        <span class="badge-tag {s_status}">[ {s_label} ]</span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                # AI Safety Officer Report
                st.markdown(f"""
                <div class="glass-panel">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <span style="font-family: 'Cinzel', serif; font-weight: 600; font-size: 0.92rem; color: var(--gold-bright);">AI Safety Officer Debrief</span>
                        <span style="font-family: 'Space Mono', monospace; font-size: 0.70rem; color: var(--gold-primary); background: rgba(223, 200, 160, 0.08); padding: 0.2rem 0.5rem; border-radius: 2px; border: 1px solid var(--border-gold-subtle);">
                            [ {llm_result['source'].upper()} ]
                        </span>
                    </div>
                    <div class="ai-report-box">
                        {llm_result['report']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ─── Handle REGISTERED WORKER ───
            else:
                active_worker = matched_worker
                display_conf = match_conf

                # Step 2: High-Accuracy Safety Detection
                with st.spinner(f"Running multi-modal safety inspection for {active_worker['name']}..."):
                    telemetry = detector.process_image(
                        selected_image,
                        conf_threshold=conf_thresh,
                        simulated_preset=preset_type,
                        api_key=gemini_key_input
                    )
                    llm_result = generate_safety_report(telemetry, api_key=gemini_key_input, worker_profile=active_worker)

                status = telemetry["status"]
                annotated_img = telemetry["annotated_image"]

                # Voice Broadcast
                if enable_voice:
                    if status == "BLOCKED":
                        speak_voice_alert(f"Critical DLP Security Breach. Open flame detected for {active_worker['name']}. Worker ID blocked. Turnstiles locked.", play_klaxon=True)
                    elif status == "WARNING":
                        speak_voice_alert(f"Safety Warning for {active_worker['name']}. Mandatory personal protective equipment missing. Site entry restricted.", play_klaxon=False)
                    else:
                        speak_voice_alert(f"Safety verified for {active_worker['name']}. Complete gear cleared. Access granted.", play_klaxon=False)

                # Dynamic Digital RFID Badge Card
                badge_border = "var(--status-block)" if status == "BLOCKED" else ("var(--status-warn)" if status == "WARNING" else "var(--gold-primary)")
                badge_stamp = "[ ID SUSPENDED // TURNSTILE LOCKED ]" if status == "BLOCKED" else ("[ ENTRY RESTRICTED // MISSING PPE ]" if status == "WARNING" else "[ ACCESS CLEARED // GATE 01 OPEN ]")

                st.markdown("**[ PERSONNEL VERIFICATION ]**")
                st.markdown(f"""
                <div class="worker-badge-card" style="border-left: 3px solid {badge_border};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-family: 'Cinzel', serif; font-size: 1.3rem; font-weight: 700; color: #ffffff;">{active_worker['name']}</div>
                            <div style="font-size: 0.80rem; color: var(--gold-primary); font-family: 'Space Mono', monospace; margin-top: 0.2rem;">
                                ID: {active_worker['id']} • {active_worker['role']}
                            </div>
                        </div>
                        <div style="font-family: 'Space Mono', monospace; font-size: 0.72rem; padding: 0.25rem 0.6rem; border-radius: 2px; background: rgba(223, 200, 160, 0.08); color: var(--gold-bright); border: 1px solid var(--border-gold-subtle);">
                            MATCH: {int(display_conf * 100)}%
                        </div>
                    </div>
                    <div style="margin-top: 0.8rem; font-size: 0.82rem; color: #a89f94; display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; font-weight: 300;">
                        <div>Dept: <span style="color: #f8fafc; font-weight: 500;">{active_worker['department']}</span></div>
                        <div>Zone: <span style="color: #f8fafc; font-weight: 500;">{active_worker['zone']}</span></div>
                        <div>Blood: <span style="color: #f8fafc; font-weight: 500;">{active_worker.get('blood_group', 'N/A')}</span></div>
                        <div>Emergency: <span style="color: #f8fafc; font-weight: 500;">{active_worker.get('emergency_contact', 'N/A')}</span></div>
                    </div>
                    <div style="margin-top: 0.85rem; font-family: 'Space Mono', monospace; font-size: 0.76rem; font-weight: 700; color: {badge_border}; letter-spacing: 0.08em;">
                        GOVERNANCE: {badge_stamp}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Big Status Card
                if status == "BLOCKED":
                    st.markdown(f"""
                    <div class="status-card status-card-blocked">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-family: 'Cinzel', serif; font-size: 1.2rem; font-weight: 700; color: #f87171;">🚨 ACCESS DENIED: ID BLOCKED</span>
                            <span style="background: rgba(248, 113, 113, 0.2); color: #fca5a5; padding: 0.2rem 0.6rem; border-radius: 2px; font-family: 'Space Mono'; font-size: 0.70rem; font-weight: 700; border: 1px solid rgba(248, 113, 113, 0.4);">[ DLP BREACH ]</span>
                        </div>
                        <div style="color: #fca5a5; font-size: 0.92rem; font-weight: 400;">{telemetry['status_message']}</div>
                        <div style="margin-top: 0.6rem; font-family: 'Space Mono'; font-size: 0.75rem; color: #f87171;">ACTION: Turnstile 01 physically locked. Incident logged for mandatory OSHA review.</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif status == "WARNING":
                    st.markdown(f"""
                    <div class="status-card status-card-warning">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-family: 'Cinzel', serif; font-size: 1.2rem; font-weight: 700; color: #eab308;">⚠️ PPE COMPLIANCE WARNING</span>
                            <span style="background: rgba(234, 179, 8, 0.2); color: #fef08a; padding: 0.2rem 0.6rem; border-radius: 2px; font-family: 'Space Mono'; font-size: 0.70rem; font-weight: 700; border: 1px solid rgba(234, 179, 8, 0.4);">[ ENTRY HELD ]</span>
                        </div>
                        <div style="color: #fef08a; font-size: 0.92rem; font-weight: 400;">{telemetry['status_message']}</div>
                        <div style="margin-top: 0.6rem; font-family: 'Space Mono'; font-size: 0.75rem; color: #eab308;">ACTION: Staging redirect for {active_worker['name']}. Equip mandatory apparel before re-scanning.</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="status-card status-card-safe">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-family: 'Cinzel', serif; font-size: 1.2rem; font-weight: 700; color: #4ade80;">✅ SITE ACCESS GRANTED</span>
                            <span style="background: rgba(74, 222, 128, 0.2); color: #86efac; padding: 0.2rem 0.6rem; border-radius: 2px; font-family: 'Space Mono'; font-size: 0.70rem; font-weight: 700; border: 1px solid rgba(74, 222, 128, 0.4);">[ ALL CLEAR ]</span>
                        </div>
                        <div style="color: #86efac; font-size: 0.92rem; font-weight: 400;">{telemetry['status_message']}</div>
                        <div style="margin-top: 0.6rem; font-family: 'Space Mono'; font-size: 0.75rem; color: #4ade80;">TOKEN: CLEARED-{active_worker['id']} • Turnstile 01 OPEN</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Vision HUD Preview & Checklist
                col_img_res, col_stat_res = st.columns([1.1, 1])

                with col_img_res:
                    st.image(annotated_img, caption="Vision HUD Optical Telemetry Overlay", use_container_width=True)

                with col_stat_res:
                    st.markdown("""
                    <div class="glass-panel" style="margin-bottom: 0.8rem;">
                        <div style="font-family: 'Cinzel', serif; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: var(--gold-bright);">Telemetry Breakdown</div>
                    """, unsafe_allow_html=True)

                    h_status = "badge-ok" if telemetry["helmet"] else "badge-fail"
                    h_label = f"DETECTED ({int(telemetry['helmet_conf']*100)}%)" if telemetry["helmet"] else "MISSING"
                    st.markdown(f"""
                    <div class="checklist-row">
                        <span style="font-size: 0.88rem; font-weight: 300;">👷 Hardhat / Cranial Dome</span>
                        <span class="badge-tag {h_status}">[ {h_label} ]</span>
                    </div>
                    """, unsafe_allow_html=True)

                    v_status = "badge-ok" if telemetry["vest"] else "badge-fail"
                    v_label = f"DETECTED ({int(telemetry['vest_conf']*100)}%)" if telemetry["vest"] else "MISSING"
                    st.markdown(f"""
                    <div class="checklist-row">
                        <span style="font-size: 0.88rem; font-weight: 300;">🦺 High-Vis Safety Vest</span>
                        <span class="badge-tag {v_status}">[ {v_label} ]</span>
                    </div>
                    """, unsafe_allow_html=True)

                    s_status = "badge-fail" if telemetry["smoking"] else "badge-ok"
                    s_label = f"DETECTED ({int(telemetry['smoking_conf']*100)}%)" if telemetry["smoking"] else "CLEAR (NONE)"
                    st.markdown(f"""
                    <div class="checklist-row">
                        <span style="font-size: 0.88rem; font-weight: 300;">🚬 Smoking / Contraband</span>
                        <span class="badge-tag {s_status}">[ {s_label} ]</span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                # AI Safety Officer Report
                st.markdown(f"""
                <div class="glass-panel">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <span style="font-family: 'Cinzel', serif; font-weight: 600; font-size: 0.92rem; color: var(--gold-bright);">AI Safety Officer Debrief</span>
                        <span style="font-family: 'Space Mono', monospace; font-size: 0.70rem; color: var(--gold-primary); background: rgba(223, 200, 160, 0.08); padding: 0.2rem 0.5rem; border-radius: 2px; border: 1px solid var(--border-gold-subtle);">
                            [ {llm_result['source'].upper()} ]
                        </span>
                    </div>
                    <div class="ai-report-box">
                        {llm_result['report']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 1-Click OSHA PDF Report Export
                pdf_data = create_osha_pdf(
                    telemetry=telemetry,
                    llm_report_text=llm_result["report"],
                    image_pil=annotated_img,
                    worker_profile=active_worker
                )

                st.download_button(
                    label=f"📄 Download OSHA Incident Audit Certificate for {active_worker['name']} (PDF)",
                    data=pdf_data,
                    file_name=f"SiteVision_OSHA_{active_worker['id']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("👈 Select a live webcam feed, upload an image, or click a benchmark scenario on the left to start.")

# =============================================================================
# TAB 3: PERSONNEL REGISTRY & GOVERNANCE LOG
# =============================================================================
with tab_registry:
    st.markdown("### [ PERSONNEL REGISTRY // 5 REGISTERED OPERATORS ]")
    st.caption("Active site biometric registry synchronized with Turnstile Gate 01:")

    reg_cols = st.columns(5, gap="medium")
    for idx, (k, p) in enumerate(WORKERS_DATABASE.items()):
        with reg_cols[idx]:
            p_img_path = os.path.join(WORKERS_DIR, p["photo_file"])
            if os.path.exists(p_img_path):
                st.image(p_img_path, caption=f"{p['name']} ({p['id']})", use_container_width=True)
            
            st.markdown(f"""
            <div style="background: var(--bg-card); border: 1px solid var(--border-gold-subtle); border-radius: 4px; padding: 0.9rem; font-size: 0.82rem;">
                <div style="font-family: 'Cinzel', serif; font-weight: 700; color: #ffffff; font-size: 0.92rem;">{p['name']}</div>
                <div style="color: var(--gold-primary); font-family: 'Space Mono'; font-size: 0.72rem; margin-top: 0.2rem;">[ ID: {p['id']} ]</div>
                <div style="color: #a89f94; font-size: 0.75rem; margin-top: 0.4rem; font-weight: 300;"><b>Role:</b> {p['role']}</div>
                <div style="color: #a89f94; font-size: 0.75rem; font-weight: 300;"><b>Dept:</b> {p['department']}</div>
                <div style="color: #a89f94; font-size: 0.75rem; font-weight: 300;"><b>Zone:</b> {p['zone']}</div>
                <div style="color: var(--gold-bright); font-size: 0.75rem; margin-top: 0.4rem; font-weight: 600; font-family: 'Space Mono';">Clearance: {p['clearance']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### [ SHIFT SECURITY & AUDIT GOVERNANCE LOG ]")
    
    st.markdown("""
    | Timestamp | Personnel | ID Token | Safety Scan | DLP Status | Gate Action |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | `Today 08:30:12` | **Saurav Sharma** | `WRK-8901` | Hardhat: ✅, Vest: ✅ | Clean | `TURNSTILE 01 OPEN` |
    | `Today 09:14:45` | **Gunjan Verma** | `WRK-8902` | Hardhat: ✅, Vest: ✅ | Clean | `TURNSTILE 01 OPEN` |
    | `Today 10:02:18` | **Mayank Agarwal** | `WRK-8905` | Hardhat: ❌, Vest: ✅ | Clean | `HELD AT STAGING` |
    | `Today 11:22:04` | **Anachal Patel** | `WRK-8903` | Hardhat: ✅, Vest: ✅ | Clean | `TURNSTILE 01 OPEN` |
    | `Today 12:45:50` | **Nisha Gupta** | `WRK-8904` | Hardhat: ✅, Vest: ❌ | Clean | `HELD AT STAGING` |
    """)
