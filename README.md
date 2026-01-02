# 🎬 YT-Shorts Automation

### **AI-Powered YouTube Shorts Generation & Scheduling Pipeline**

An end-to-end **AI-driven pipeline** that automates the creation, rendering, and scheduling of motivational YouTube Shorts. Built with clean architecture and modular Python practices for high-performance content creation.

---

## 🏗️ Project Structure

```
.
├── app/
│   ├── ai_workflow/          # OpenAI script & metadata generation
│   ├── media/                # Video processing (MoviePy 2.x engine)
│   ├── shorts_uploader/      # YouTube API & OAuth scheduling
│   ├── utils/                # Loggers, JSON helpers, and file tools
│   └── config/               # Centralized Settings & Path management
├── assets/
│   ├── videos/               # 🎬 Source background clips (REQUIRED)
│   ├── musics/               # 🎵 Background music files (REQUIRED)
│   ├── logo/                 # 🟥 Branding logo: logo.png (REQUIRED)
│   └── fonts/                # Custom .ttf files for text overlays
├── data/
│   ├── generated/            # Production workspace for new reels
│   └── uploaded_reels/       # Archive for successfully posted content
├── youtube_secret/
    ├── youtube_secret.json   # YouTube OAuth2 Credentials
├── logs/                     # Rotating application logs
├── .env                      # Secret API keys (OpenAI)
├── requirements.txt          # Modern dependency lockfile
├── run_pipeline.py           # Main pipeline entry point
└── README.md
```

---

## 📦 Requirements & Modern Stack

This project utilizes the latest stable ecosystem libraries (Late 2025).

**Core Dependencies:**

- **Python 3.10+**
- **MoviePy 2.2.1+**: Transitioned to standardized functional video editing
- **LangChain 1.2.0**: Modular AI orchestration via `langchain_core`
- **OpenAI 1.109.1+**: Support for the latest reasoning models and APIs

### Installation

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Configuration

All application settings are centralized in the app/config/settings.py module. You can modify these configurations as needed.

### 📺 YouTube Settings
- **OAuth Scope**: `youtube.upload`
- **Client Secrets**: `youtube_secret/secret.json`
- **Token File**: `youtube_secret/token.pickle`
- **Publish Times (UTC +5:30)**: `06:00`, `13:00`, `18:00`, `21:00`
- **Default Tags**: shorts, motivation, inspiration

### 🎞️ Video Settings
- **Resolution**: `1080 × 1920` (Vertical)
- **FPS**: `30`
- **Duration**: `2.0s`
- **GPU Acceleration**: `h264_nvenc`
- **Fade Duration**: `0.3s`
- **Overlay Opacity**: `0.6`

### 🤖 AI Settings
- **Model**: `gpt-4o`
- **Temperature**: `0.5`
- **Responses**: `1`
- **API Key**: Loaded from `OPENAI_API_KEY`

### 📂 File & Paths
- **Assets**: `assets/`
- **Generated Reels**: `data/generated/reels/`
- **Uploaded Reels**: `data/uploaded_reels/`
- **Logs**: `logs/`

## 🔧 Setup Instructions

### 1. Media Preparation

- **Note**: On the first run, the script automatically creates the required project directory structure.
- **Backgrounds**: Place vertical (9:16) clips in `assets/videos/`
- **Audio**: Add music to `assets/musics/`
- **Branding**: Ensure your watermark is located at `assets/logo/logo.png`

### 2. Secrets Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
ENV=development
```

Download your OAuth 2.0 Client ID from the Google Cloud Console and save it as `youtube_secret.json` in the project root.

---

## 🧠 Automation Logic & Code Fixes

### MoviePy 2.x Compatibility

Code logic in `media/processor.py` has been updated to support the 2.x functional API:

- **Audio Scaling**: Uses `.with_volume_scaled()` instead of `.volumex()`
- **Positioning**: Uses `.with_position()` instead of `.set_pos()`
- **Static Assets**: Uses `ImageClip` for logos to prevent duration-related `OSError` crashes
- **Scene Effects**: Implements `vfx.FadeIn` and `vfx.FadeOut` via the `.with_effects()` list

---

## ▶️ Execution

To start the pipeline, simply run the entry point:

```bash
python run_pipeline.py
```

### Execution Pipeline

1. **AI Scripting**: Generates viral hooks and body text using LLMs
2. **Video Synthesis**: Scales clips to 1080x1920, adds overlays, and syncs audio
3. **Scheduling**: Authenticates and uploads to YouTube via OAuth2
4. **Cleanup**: Moves the final `.mp4` to `data/uploaded_reels/` and clears temporary metadata

---

## 📄 License

Educational use only.

---

**Need help?** Consider generating a script that verifies your environment (FFmpeg, API keys, folder structure) before running the main pipeline.