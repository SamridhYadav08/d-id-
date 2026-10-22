import streamlit as st
import requests
import time
import base64
import os
import datetime
from dotenv import load_dotenv

# ── Load environment variables (.env) if present ──────────────────────────────
load_dotenv()

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="D-ID Studio | AI Talking Avatar Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom Styling (Modern Glassmorphic UI with Plus Jakarta Sans) ─────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Clean up default Streamlit headers */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero header banner */
    .hero-container {
        padding: 1.6rem 2rem;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.12) 0%, rgba(6, 182, 212, 0.10) 50%, rgba(59, 130, 246, 0.08) 100%);
        border-radius: 18px;
        border: 1px solid rgba(6, 182, 212, 0.25);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 50%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .hero-subtitle {
        color: #64748B;
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.35rem;
        margin-bottom: 0.3rem;
    }
    .badge-primary {
        background-color: rgba(79, 70, 229, 0.12);
        color: #4338CA;
        border: 1px solid rgba(79, 70, 229, 0.25);
    }
    .badge-cyan {
        background-color: rgba(6, 182, 212, 0.12);
        color: #0891B2;
        border: 1px solid rgba(6, 182, 212, 0.25);
    }
    .badge-success {
        background-color: rgba(16, 185, 129, 0.12);
        color: #059669;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .badge-neutral {
        background-color: rgba(148, 163, 184, 0.14);
        color: #475569;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }

    /* Avatar preview image styling */
    .avatar-preview-box {
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        border: 1px solid rgba(128,128,128,0.2);
        transition: transform 0.2s ease;
    }
    .avatar-preview-box:hover {
        transform: scale(1.01);
    }

    /* Primary Generate Button styling */
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%) !important;
        border: none !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.65rem 2rem !important;
        box-shadow: 0 4px 18px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.45) !important;
    }

    /* Container cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1px solid rgba(128, 128, 128, 0.18) !important;
        padding: 1.2rem !important;
        background: rgba(128, 128, 128, 0.02) !important;
        transition: box-shadow 0.2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── API Constants ─────────────────────────────────────────────────────────────
DID_API_URL = "https://api.d-id.com"

# ── Voice Catalog (Microsoft Azure Neural Voices via D-ID) ────────────────────
VOICE_CATALOG = {
    "🇺🇸 English (US)": {
        "Jenny (Female - Warm & Natural)": "en-US-JennyNeural",
        "Guy (Male - Confident & Friendly)": "en-US-GuyNeural",
        "Aria (Female - Expressive)": "en-US-AriaNeural",
        "Davis (Male - Professional)": "en-US-DavisNeural",
    },
    "🇬🇧 English (UK)": {
        "Sonia (Female - Polite & Clear)": "en-GB-SoniaNeural",
        "Ryan (Male - Formal)": "en-GB-RyanNeural",
    },
    "🇦🇺 English (Australia)": {
        "Natasha (Female - Casual)": "en-AU-NatashaNeural",
        "William (Male - Relaxed)": "en-AU-WilliamNeural",
    },
    "🇮🇳 English (India)": {
        "Neerja (Female - Warm)": "en-IN-NeerjaNeural",
        "Prabhat (Male - Clear)": "en-IN-PrabhatNeural",
    },
    "🇪🇸 Spanish (Spain)": {
        "Elvira (Female - Natural)": "es-ES-ElviraNeural",
        "Alvaro (Male - Professional)": "es-ES-AlvaroNeural",
    },
    "🇲🇽 Spanish (Mexico)": {
        "Dalia (Female - Expressive)": "es-MX-DaliaNeural",
        "Jorge (Male - Warm)": "es-MX-JorgeNeural",
    },
    "🇫🇷 French (France)": {
        "Denise (Female - Clear)": "fr-FR-DeniseNeural",
        "Henri (Male - Formal)": "fr-FR-HenriNeural",
    },
    "🇩🇪 German (Germany)": {
        "Katja (Female - Precise)": "de-DE-KatjaNeural",
        "Conrad (Male - Confident)": "de-DE-ConradNeural",
    },
    "🇮🇹 Italian (Italy)": {
        "Elsa (Female - Melodic)": "it-IT-ElsaNeural",
        "Diego (Male - Expressive)": "it-IT-DiegoNeural",
    },
    "🇧🇷 Portuguese (Brazil)": {
        "Francisca (Female - Friendly)": "pt-BR-FranciscaNeural",
        "Antonio (Male - Natural)": "pt-BR-AntonioNeural",
    },
    "🇮🇳 Hindi": {
        "Swara (Female - Clear)": "hi-IN-SwaraNeural",
        "Madhur (Male - Confident)": "hi-IN-MadhurNeural",
    },
    "🇯🇵 Japanese": {
        "Nanami (Female - Soft)": "ja-JP-NanamiNeural",
        "Keita (Male - Polite)": "ja-JP-KeitaNeural",
    },
    "🇨🇳 Chinese (Mandarin)": {
        "Xiaoxiao (Female - Warm)": "zh-CN-XiaoxiaoNeural",
        "Yunxi (Male - Lively)": "zh-CN-YunxiNeural",
    },
    "🇸🇦 Arabic (Saudi Arabia)": {
        "Zariyah (Female - Clear)": "ar-SA-ZariyahNeural",
        "Hamed (Male - Formal)": "ar-SA-HamedNeural",
    },
}

VOICE_STYLE_OPTIONS = [
    "general", "cheerful", "empathetic", "excited",
    "friendly", "hopeful", "sad", "shouting",
    "terrified", "unfriendly", "whispering"
]

# ── Preset Script Templates ───────────────────────────────────────────────────
SCRIPT_TEMPLATES = {
    "✨ Default Demo": (
        "Hello! This is a demonstration of the D-ID AI avatar video generation API. "
        "Using just a portrait photo and spoken audio, D-ID creates a lifelike talking presenter. "
        "Thank you for watching!"
    ),
    "🚀 Product Pitch": (
        "Are you looking for a faster, smarter way to engage your audience? "
        "With AI-generated avatars, you can produce personalized video communications "
        "at scale in minutes, without expensive studio equipment."
    ),
    "👋 Welcome & Onboarding": (
        "Welcome to our platform! We are so glad to have you on board. "
        "Take a look around, explore our interactive features, and don't hesitate "
        "to reach out if you need any assistance along the way."
    ),
    "🎓 Educational Explainer": (
        "Did you know that modern deep learning models can synthesize facial lip synchronization "
        "directly from audio phonemes? This technology brings educational characters "
        "and digital instructors to life in over one hundred languages."
    ),
    "💡 Motivational Quote": (
        "Success is not final, failure is not fatal: it is the courage to continue that counts. "
        "Believe in your potential and make today extraordinary!"
    ),
}

# ── Demo Portrait Avatars ─────────────────────────────────────────────────────
DEMO_AVATARS = {
    "Sarah (Tech Executive)": {
        "url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&auto=format&fit=crop&q=80",
        "desc": "Professional studio headshot with clear frontal lighting."
    },
    "Marcus (Product Lead)": {
        "url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&auto=format&fit=crop&q=80",
        "desc": "Warm, confident male portrait suited for product walkthroughs."
    },
    "Elena (Creative Director)": {
        "url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600&auto=format&fit=crop&q=80",
        "desc": "Expressive portrait ideal for marketing campaigns and announcements."
    },
    "David (Keynote Host)": {
        "url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600&auto=format&fit=crop&q=80",
        "desc": "Authoritative studio portrait perfect for educational explainers."
    }
}

# ── Initialize Session State ──────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "script_content" not in st.session_state:
    st.session_state.script_content = SCRIPT_TEMPLATES["✨ Default Demo"]

# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

def get_configured_api_key() -> str:
    """Read API key from Streamlit Secrets or environment variable with fallback."""
    # 1. Check Streamlit Secrets (for Streamlit Community Cloud)
    try:
        if "DID_API_KEY" in st.secrets and st.secrets["DID_API_KEY"]:
            return st.secrets["DID_API_KEY"]
    except Exception:
        pass
    # 2. Check local environment variable (.env)
    return os.getenv("DID_API_KEY", "")


def build_auth_header(api_key: str, is_multipart: bool = False) -> dict:
    """Format HTTP Basic authentication header reliably for D-ID."""
    api_key = api_key.strip()
    if api_key.lower().startswith("basic "):
        api_key = api_key[6:].strip()

    if ":" in api_key:
        token = base64.b64encode(api_key.encode()).decode()
    else:
        token = api_key

    headers = {"Authorization": f"Basic {token}"}
    if not is_multipart:
        headers["Content-Type"] = "application/json"
    return headers


def fetch_account_credits(api_key: str) -> dict | None:
    """Check remaining account credits and status from D-ID GET /credits."""
    headers = build_auth_header(api_key)
    try:
        resp = requests.get(f"{DID_API_URL}/credits", headers=headers, timeout=12)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        st.sidebar.error(f"Credit check failed ({resp.status_code}): {resp.text}")
        return None
    except Exception as e:
        st.sidebar.error(f"Connection error: {e}")
        return None


def upload_image(api_key: str, file_bytes: bytes, file_name: str = "avatar.jpg") -> str | None:
    """Upload portrait image file to D-ID POST /images."""
    headers = build_auth_header(api_key, is_multipart=True)
    files = {"image": (file_name, file_bytes, "image/jpeg")}
    try:
        resp = requests.post(f"{DID_API_URL}/images", headers=headers, files=files, timeout=35)
        resp.raise_for_status()
        return resp.json().get("url")
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Avatar image upload failed ({resp.status_code}): {resp.text}")
        return None
    except Exception as e:
        st.error(f"❌ Image upload error: {e}")
        return None


def upload_audio(api_key: str, audio_bytes: bytes, audio_name: str = "speech.mp3") -> str | None:
    """Upload custom speech audio file to D-ID POST /audios."""
    headers = build_auth_header(api_key, is_multipart=True)
    mime = "audio/mpeg"
    if audio_name.lower().endswith(".wav"):
        mime = "audio/wav"
    elif audio_name.lower().endswith(".m4a"):
        mime = "audio/m4a"
    elif audio_name.lower().endswith(".ogg"):
        mime = "audio/ogg"

    files = {"audio": (audio_name, audio_bytes, mime)}
    try:
        resp = requests.post(f"{DID_API_URL}/audios", headers=headers, files=files, timeout=45)
        resp.raise_for_status()
        return resp.json().get("url")
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Audio file upload failed ({resp.status_code}): {resp.text}")
        return None
    except Exception as e:
        st.error(f"❌ Audio upload error: {e}")
        return None


def create_talk(
    api_key: str,
    source_url: str,
    audio_mode: str,
    script_text: str = "",
    voice_id: str = "",
    voice_style: str = "general",
    audio_url: str = "",
    stitch: bool = True,
) -> dict | None:
    """Submit a video generation job to D-ID POST /talks."""
    headers = build_auth_header(api_key)

    if audio_mode == "audio":
        script_payload = {
            "type": "audio",
            "audio_url": audio_url
        }
    else:
        script_payload = {
            "type": "text",
            "input": script_text,
            "provider": {
                "type": "microsoft",
                "voice_id": voice_id,
                "voice_config": {"style": voice_style},
            },
        }

    config_payload = {
        "fluent": True,
        "pad_audio": 0.0,
        "stitch": stitch,
        "result_format": "mp4"
    }

    payload = {
        "source_url": source_url,
        "script": script_payload,
        "config": config_payload,
    }

    try:
        resp = requests.post(f"{DID_API_URL}/talks", json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ D-ID API Error ({resp.status_code}): {resp.text}")
        return None
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
        return None


def poll_until_done(api_key: str, talk_id: str, max_wait: int = 180, interval: int = 3) -> dict | None:
    """Poll job status until 'done' or 'error'."""
    elapsed = 0
    headers = build_auth_header(api_key)
    progress_bar = st.progress(0, text="⏳ Initializing neural renderer...")

    while elapsed < max_wait:
        try:
            resp = requests.get(f"{DID_API_URL}/talks/{talk_id}", headers=headers, timeout=15)
            resp.raise_for_status()
            result = resp.json()
        except Exception:
            result = None

        if result is None:
            time.sleep(interval)
            elapsed += interval
            continue

        status = result.get("status", "unknown")

        if status == "done":
            progress_bar.progress(100, text="✨ Video rendering complete!")
            time.sleep(0.4)
            progress_bar.empty()
            return result
        elif status in ("error", "rejected"):
            progress_bar.empty()
            st.error(f"❌ Video generation failed: {result.get('error', result)}")
            return None

        pct = min(int((elapsed / max_wait) * 95), 95)
        progress_bar.progress(pct, text=f"🎥 Synthesizing lip-sync... ({status.capitalize()} - {elapsed}s)")
        time.sleep(interval)
        elapsed += interval

    st.error("⏱️ Timed out waiting for the video. Please check your D-ID dashboard.")
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar Controls & API Settings
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Studio Settings")
    st.markdown(
        "<span class='badge badge-primary'>D-ID V2 API</span>"
        "<span class='badge badge-cyan'>Azure Neural TTS</span>",
        unsafe_allow_html=True
    )
    
    st.markdown("---")

    configured_key = get_configured_api_key()
    api_key_input = st.text_input(
        "D-ID API Key",
        value=configured_key,
        type="password",
        placeholder="Basic ... or username:password",
        help="Get your key at studio.d-id.com → Profile → API. You can also configure DID_API_KEY in .env or Streamlit Secrets."
    )
    api_key = api_key_input.strip()

    if api_key:
        st.success("API Key detected", icon="🟢")
    else:
        st.info("💡 Enter your API key above or in `.env` to start.", icon="🔑")

    # Live Credit & Account Checker
    st.markdown("#### 💳 Account & Credits")
    if st.button("Check Credits & Plan", use_container_width=True):
        if not api_key:
            st.warning("Please provide a valid API key first.")
        else:
            with st.spinner("Checking D-ID credits..."):
                credits_info = fetch_account_credits(api_key)
                if credits_info:
                    st.success("Connected to D-ID API", icon="✅")
                    
                    # Display structured stats if available
                    remaining = credits_info.get("remaining", credits_info.get("total", "N/A"))
                    total = credits_info.get("total", "N/A")
                    
                    c_col1, c_col2 = st.columns(2)
                    with c_col1:
                        st.metric("Remaining", remaining)
                    with c_col2:
                        st.metric("Total Limit", total)
                        
                    with st.expander("🔍 Account Details (JSON)"):
                        st.json(credits_info)

    st.markdown("---")
    st.markdown("#### 💡 Pro Tips")
    st.markdown("""
    - **Avatar Quality**: Front-facing, high-res portraits with neutral expression yield the best lip-sync.
    - **Audio Pacing**: Keep TTS scripts between 15 and 90 words for punchy, high-engagement videos.
    - **Audio Uploads**: Use clean speech audio (`.mp3` or `.wav`) with low background noise.
    """)

    st.markdown("---")
    st.caption("D-ID AI Avatar Studio • Built with Streamlit")


# ─────────────────────────────────────────────────────────────────────────────
# Main Application Area
# ─────────────────────────────────────────────────────────────────────────────

# Header Hero
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🎬 AI Avatar Video Studio</div>
    <div class="hero-subtitle">Transform portrait photos into photorealistic talking presenters with neural voice synthesis and custom voiceovers.</div>
</div>
""", unsafe_allow_html=True)

# Main Grid: Left column for Avatar Photo, Right column for Voice & Script Content
col_avatar, col_content = st.columns([1, 1.25], gap="large")

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Avatar Presenter
# ─────────────────────────────────────────────────────────────────────────────
with col_avatar:
    with st.container(border=True):
        st.subheader("1️⃣ Avatar Presenter")
        st.caption("Select a studio demo presenter or upload any custom face photo.")

        avatar_tab1, avatar_tab2 = st.tabs(["📸 Upload Photo", "🌟 Demo Presenters"])

        uploaded_file = None
        selected_demo_name = None
        chosen_source_url = None

        with avatar_tab1:
            uploaded_file = st.file_uploader(
                "Upload portrait photo (JPG, PNG)",
                type=["jpg", "jpeg", "png"],
                help="Front-facing portrait photos with good lighting work best.",
                label_visibility="collapsed"
            )
            if uploaded_file is not None:
                st.image(uploaded_file, caption=f"Selected: {uploaded_file.name}", use_container_width=True)
                st.markdown(
                    f"<span class='badge badge-success'>Ready to Upload</span>"
                    f"<span class='badge badge-neutral'>{round(uploaded_file.size / 1024, 1)} KB</span>",
                    unsafe_allow_html=True
                )

        with avatar_tab2:
            selected_demo_name = st.selectbox(
                "Choose a pre-tested studio avatar:",
                options=list(DEMO_AVATARS.keys()),
                index=0
            )
            demo_info = DEMO_AVATARS[selected_demo_name]
            st.image(demo_info["url"], caption=demo_info["desc"], use_container_width=True)
            st.caption(f"_{selected_demo_name}_")

        # Determine effective avatar image
        has_custom_upload = (uploaded_file is not None)
        if not has_custom_upload and selected_demo_name:
            chosen_source_url = DEMO_AVATARS[selected_demo_name]["url"]


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 & 3: Spoken Content & Voice Synthesis
# ─────────────────────────────────────────────────────────────────────────────
with col_content:
    with st.container(border=True):
        st.subheader("2️⃣ Voice & Content Synthesis")
        st.caption("Synthesize speech with multilingual Azure Neural Voices or provide your own voice track.")

        mode_tab_tts, mode_tab_audio = st.tabs(["✍️ Neural Text-to-Speech (TTS)", "🎙️ Custom Audio & Mic"])

        text_to_speak = ""
        voice_id = "en-US-JennyNeural"
        voice_style = "general"
        uploaded_audio_file = None
        recorded_audio = None
        is_audio_mode = False

        # --- Tab A: Neural TTS ---
        with mode_tab_tts:
            t_col1, t_col2 = st.columns([1.5, 1])
            with t_col1:
                selected_template = st.selectbox(
                    "⚡ Load a Preset Script:",
                    list(SCRIPT_TEMPLATES.keys()),
                    index=0
                )
            with t_col2:
                st.write("")
                st.write("")
                if st.button("Apply Template", use_container_width=True):
                    st.session_state.script_content = SCRIPT_TEMPLATES[selected_template]
                    st.rerun()

            script_text = st.text_area(
                "Spoken Script Editor:",
                value=st.session_state.script_content,
                height=150,
                max_chars=1200,
                placeholder="Type or paste the words your presenter will speak...",
                help="Maximum 1,200 characters per video generation."
            )
            st.session_state.script_content = script_text
            text_to_speak = script_text

            # Live Script Metrics
            word_count = len(text_to_speak.split()) if text_to_speak.strip() else 0
            char_count = len(text_to_speak)
            est_duration = round((word_count / 140) * 60) if word_count > 0 else 0

            st.markdown(
                f"<span class='badge badge-primary'>{char_count} Characters</span>"
                f"<span class='badge badge-cyan'>{word_count} Words</span>"
                f"<span class='badge badge-neutral'>Est. ~{est_duration}s speech</span>",
                unsafe_allow_html=True
            )

            st.markdown("---")

            # Voice & Language Selectors
            st.markdown("##### 🌐 Neural Voice & Emotion")
            v_col1, v_col2 = st.columns(2)
            with v_col1:
                selected_lang = st.selectbox("Language / Accent", list(VOICE_CATALOG.keys()))
                available_voices = VOICE_CATALOG[selected_lang]
                selected_voice_label = st.selectbox("Voice Talent", list(available_voices.keys()))
                voice_id = available_voices[selected_voice_label]

            with v_col2:
                voice_style = st.selectbox(
                    "Emotional Tone",
                    VOICE_STYLE_OPTIONS,
                    index=0,
                    help="Azure Neural speech emotion style."
                )
                st.info(f"🗣️ Active: **{voice_id}**\n\n🎭 Tone: **{voice_style.capitalize()}**")

        # --- Tab B: Custom Audio / Microphone Recording ---
        with mode_tab_audio:
            is_audio_mode = True
            st.markdown("##### 🎙️ Upload or Record Custom Audio Track")
            st.caption("Provide pre-recorded audio or record straight from your microphone.")

            if hasattr(st, "audio_input"):
                recorded_audio = st.audio_input("Record voice directly:")

            uploaded_audio_file = st.file_uploader(
                "Or upload an audio file (.mp3, .wav, .m4a, .ogg)",
                type=["mp3", "wav", "m4a", "ogg"],
                help="Clean vocal audio without heavy background music produces the best results."
            )

            active_audio = recorded_audio if recorded_audio is not None else uploaded_audio_file
            if active_audio:
                st.audio(active_audio)
                st.success(f"Audio ready: **{getattr(active_audio, 'name', 'Recorded Microphone Audio')}**", icon="✅")
            else:
                st.info("Upload or record audio to lip-sync your presenter.")

    # ── Advanced Animation Settings ───────────────────────────────────────────
    with st.expander("⚙️ Advanced Animation Settings", expanded=False):
        adv_col1, adv_col2 = st.columns(2)
        with adv_col1:
            stitch_option = st.checkbox(
                "Full-Body Seamless Stitching (`stitch`)",
                value=True,
                help="When enabled, seamlessly animates the head on top of the original full photo. When disabled, crops tightly to the head."
            )
        with adv_col2:
            custom_title = st.text_input(
                "Video Project Label",
                value="Studio Presenter Take",
                help="Title label to organize generations in your session library."
            )


# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Video Generation Trigger
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
action_col1, action_col2, action_col3 = st.columns([1, 2, 1])

with action_col2:
    generate_btn = st.button(
        "🚀 Generate AI Avatar Video", 
        type="primary", 
        use_container_width=True
    )

if generate_btn:
    # ── Input Validation ──────────────────────────────────────────────────────
    errors = []
    if not api_key:
        errors.append("Please enter your D-ID API Key in the sidebar or set DID_API_KEY in `.env`.")

    if not has_custom_upload and not chosen_source_url:
        errors.append("Please upload a portrait image or select a demo presenter in Step 1.")

    if is_audio_mode and (recorded_audio is not None or uploaded_audio_file is not None):
        # Audio mode chosen and audio is present
        pass
    else:
        # TTS mode
        if not text_to_speak.strip():
            errors.append("Please enter a spoken script in the editor (Step 2).")

    if errors:
        for err in errors:
            st.error(f"⚠️ {err}")
        st.stop()

    # ── Execution Pipeline ────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🎬 Video Generation in Progress")

    with st.status("🚀 Processing assets with D-ID...", expanded=True) as status_box:
        # 1. Source Image Resolution
        if has_custom_upload:
            st.write("📤 Uploading custom avatar photo to D-ID cloud storage...")
            source_url = upload_image(api_key, uploaded_file.getvalue(), uploaded_file.name)
            if not source_url:
                status_box.update(label="❌ Failed to upload avatar image", state="error")
                st.stop()
            st.write("✅ Avatar photo uploaded successfully.")
        else:
            st.write("🌟 Using selected studio demo presenter...")
            source_url = chosen_source_url

        # 2. Audio Processing (if custom audio used)
        audio_url = ""
        audio_mode_key = "text"
        chosen_audio_track = recorded_audio if recorded_audio is not None else uploaded_audio_file

        if chosen_audio_track is not None and (is_audio_mode or not text_to_speak.strip()):
            audio_mode_key = "audio"
            st.write("🎙️ Uploading custom audio track to D-ID servers...")
            audio_name = getattr(chosen_audio_track, "name", "speech.wav")
            audio_url = upload_audio(api_key, chosen_audio_track.getvalue(), audio_name)
            if not audio_url:
                status_box.update(label="❌ Failed to upload custom audio", state="error")
                st.stop()
            st.write("✅ Custom audio track uploaded successfully.")

        # 3. Dispatch Create Talk Job
        st.write("⚙️ Submitting animation job to D-ID neural render engine...")
        job = create_talk(
            api_key=api_key,
            source_url=source_url,
            audio_mode=audio_mode_key,
            script_text=text_to_speak,
            voice_id=voice_id,
            voice_style=voice_style,
            audio_url=audio_url,
            stitch=stitch_option,
        )

        if not job or not job.get("id"):
            status_box.update(label="❌ Failed to dispatch generation job", state="error")
            st.stop()

        talk_id = job.get("id")
        st.write(f"✅ Render job queued! Talk ID: `{talk_id}`")
        status_box.update(label="🎥 Rendering lip-synced video on D-ID neural servers...", state="running")

    # 4. Polling until complete
    result = poll_until_done(api_key, talk_id)

    if result and result.get("result_url"):
        video_url = result.get("result_url")

        # Save to session history
        history_entry = {
            "id": talk_id,
            "url": video_url,
            "timestamp": datetime.datetime.now().strftime("%I:%M %p - %b %d"),
            "title": custom_title.strip() or f"Avatar Video #{len(st.session_state.history) + 1}",
            "type": "Custom Audio" if audio_mode_key == "audio" else f"TTS ({voice_id})",
            "preview_text": (text_to_speak[:85] + "...") if text_to_speak else "Custom Audio Track"
        }
        st.session_state.history.insert(0, history_entry)
    else:
        st.error("Video processing failed or timed out. Please check your credit balance or try again.")


# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Output Review & Public Share Link
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[0]
    
    st.divider()
    st.subheader("🎉 Step 5 · Review Output & Public Share Link")

    with st.container(border=True):
        out_col1, out_col2 = st.columns([1.3, 1], gap="medium")

        with out_col1:
            st.video(latest["url"])

        with out_col2:
            st.markdown("#### 🔗 Public Shareable Link")
            st.caption("Copy this URL directly to share your creation or submit your assignment:")
            st.code(latest["url"], language=None)

            btn_grid1, btn_grid2 = st.columns(2)
            with btn_grid1:
                st.link_button("🌐 Open in Browser", latest["url"], use_container_width=True)
            with btn_grid2:
                try:
                    with st.spinner("Preparing MP4..."):
                        video_bytes = requests.get(latest["url"], timeout=40).content
                        st.download_button(
                            "⬇️ Download MP4",
                            data=video_bytes,
                            file_name=f"did_avatar_{latest['id']}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                except Exception:
                    pass

            # Embed Code Snippet
            with st.expander("📋 Copy HTML Embed Code"):
                embed_code = f'<video width="640" height="360" controls><source src="{latest["url"]}" type="video/mp4"></video>'
                st.code(embed_code, language="html")

    st.success("✨ Your AI avatar video is ready and verified!", icon="🚀")


# ─────────────────────────────────────────────────────────────────────────────
# Session Gallery: Generation History
# ─────────────────────────────────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.divider()
    top_h_col1, top_h_col2 = st.columns([3, 1])
    with top_h_col1:
        st.subheader(f"🎞️ Session Video Library ({len(st.session_state.history)})")
        st.caption("Review and compare all talking avatar videos generated during your current session.")
    with top_h_col2:
        st.write("")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    for idx, item in enumerate(st.session_state.history[1:], start=2):
        with st.expander(f"🎬 #{idx} | {item['title']} · {item['timestamp']} ({item['type']})", expanded=False):
            h_col1, h_col2 = st.columns([1, 1.4])
            with h_col1:
                st.video(item["url"])
            with h_col2:
                st.markdown(f"**Script / Audio:** {item['preview_text']}")
                st.markdown(f"**Talk ID:** `{item['id']}`")
                st.markdown("**Public Share Link:**")
                st.code(item["url"], language=None)
                
                h_b1, h_b2 = st.columns(2)
                with h_b1:
                    st.link_button("🌐 Open Link", item["url"], use_container_width=True)
                with h_b2:
                    try:
                        v_data = requests.get(item["url"], timeout=30).content
                        st.download_button(
                            "⬇️ Download MP4",
                            data=v_data,
                            file_name=f"{item['title'].replace(' ', '_')}_{idx}.mp4",
                            mime="video/mp4",
                            key=f"dl_hist_{item['id']}_{idx}",
                            use_container_width=True
                        )
                    except Exception:
                        pass

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94A3B8; font-size: 0.85rem; padding: 1rem 0;'>"
    "D-ID AI Avatar Video Studio • Powered by D-ID API, Microsoft Azure Neural TTS & Streamlit"
    "</div>",
    unsafe_allow_html=True
)
