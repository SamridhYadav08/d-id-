# 🎬 D-ID AI Avatar Video Studio

A modern, full-featured [Streamlit](https://streamlit.io/) application that turns portrait photos into photorealistic talking AI avatar videos using the [D-ID API](https://docs.d-id.com/) and Microsoft Azure Neural Text-to-Speech (TTS).

---

## ✨ Features & Capabilities

- **🎨 Modern Glassmorphic UI:** Clean, responsive design crafted with Plus Jakarta Sans typography, sleek gradient styling, and real-time status badges.
- **📸 Flexible Avatar Input:**
  - **Custom Image Upload:** Drag & drop any front-facing portrait photo (`.jpg`, `.jpeg`, `.png`) with file size validation.
  - **Curated Demo Presenters:** Instant access to 4 pre-tested, studio-quality demo avatar portraits for quick testing.
- **🗣️ Multi-Mode Voice & Speech Synthesis:**
  - **✍️ Neural Text-to-Speech (TTS):**
    - **1-Click Script Templates:** Fast presets for Product Pitches, Educational Explainers, Welcome Greetings, and Motivational Quotes.
    - **Real-Time Analytics:** Live character counter, word counter, and estimated speech playback duration.
    - **Global Voice Catalog:** 14+ languages and accents (US, UK, Australia, India, Spain, Mexico, France, Germany, Italy, Brazil, Hindi, Japanese, Chinese, Arabic).
    - **Emotional Tone Styles:** Cheerful, empathetic, excited, friendly, hopeful, whispering, and more.
  - **🎙️ Custom Audio & Voiceover:**
    - Live microphone voice recording via Streamlit's native audio input.
    - Drag-and-drop file uploader for `.mp3`, `.wav`, `.m4a`, and `.ogg` files.
- **💳 Live Account & Credit Checker:** Check real-time D-ID credits, limits, and plan details directly from the sidebar (`GET /credits`).
- **⚙️ Advanced Animation Tuning:** Seamless full-body photo stitching (`config.stitch`) vs close-up facial crop.
- **🔗 Share & Export Suite (Step 5):**
  - Instant high-definition video player.
  - Public shareable URL in a 1-click code block.
  - "Open in Browser" button.
  - Direct local MP4 video file downloader.
  - HTML `<video>` embed snippet generator.
- **🎞️ Session History & Video Library:** Preserves generated videos across the session so you can review, compare, re-download, or copy links anytime.
- **🔒 Flexible Secret Management:** Automatically loads keys from local `.env` files or Streamlit Community Cloud Secrets (`st.secrets`).

---

## 📋 Assignment Steps Covered

| Step | Implementation |
|---|---|
| **Step 1: Select or create a suitable avatar** | Upload any custom portrait photo or pick from studio-tested demo avatars. |
| **Step 2: Add a short script or spoken content** | Custom script editor with templates and duration estimates, or custom voiceover/mic recording. |
| **Step 3: Configure voice and language** | Multilingual Azure Neural voices, regional dialects, and emotional voice styling. |
| **Step 4: Generate the AI avatar video** | Dispatches job to `POST /talks`, real-time status tracker, and progress bar animation. |
| **Step 5: Review output & copy public link** | Video player, verified public URL code box, MP4 downloader, and HTML embed snippet. |

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/your-username/d-id-avatar-studio.git
cd d-id-avatar-studio
```

### 2. Set up a virtual environment (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your D-ID API Key
Copy `.env.example` to `.env` and add your key:
```bash
cp .env.example .env
```
Inside `.env`:
```ini
DID_API_KEY=your_d_id_api_key_here
```
> **Where to find your key:** Log in to [studio.d-id.com](https://studio.d-id.com/) → Click your profile icon → Select **API**.

*(You can also paste your API key directly into the sidebar text box inside the app).*

### 5. Launch the Studio
```bash
python -m streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this project to GitHub (ensure `.env` is ignored by `.gitignore`).
2. Visit [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select your repository, branch, and set the main file path to `app.py`.
4. In **Advanced Settings → Secrets**, configure:
   ```toml
   DID_API_KEY = "your_d_id_api_key_here"
   ```
5. Click **Deploy**. Your live app will automatically detect and authenticate with your key!

---

## 📁 Project Structure

```
Did/
├── app.py            # Streamlit application with full utilities & modern UI
├── requirements.txt  # Dependencies (streamlit, requests, python-dotenv)
├── .env.example      # Environment variable template
├── .gitignore        # Ignores secrets, caches, and virtual envs
├── LICENSE           # MIT License
└── README.md         # Documentation & setup guide
```

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [D-ID REST API v2](https://docs.d-id.com/)
- [Microsoft Azure Neural TTS](https://azure.microsoft.com/en-us/products/ai-services/ai-speech)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Requests](https://requests.readthedocs.io/)

---

## 📄 License
[MIT](LICENSE)
