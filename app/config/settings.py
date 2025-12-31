from pathlib import Path
import logging
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# Base Directories
# -----------------------------
BASE_DIR: Path = Path(__file__).resolve().parents[2]
ASSETS_DIR: Path = BASE_DIR / "assets"
DATA_DIR: Path = BASE_DIR / "data"
DATA_GENERATED_DIR: Path = DATA_DIR / "generated"

# -----------------------------
# Logging Configuration
# -----------------------------
LOG_LEVEL = logging.DEBUG if os.getenv("ENV") == "development" else logging.INFO

# -----------------------------
# Video Generation Settings
# -----------------------------
@dataclass
class VideoConfig:
    target_width: int = 1080
    target_height: int = 1920
    video_duration: float = 2.0
    fade_duration: float = 0.3
    text_font_size: int = 40
    hook_font_size: int = 40
    logo_width: int = 200
    logo_margin_bottom: int = 250
    fps: int = 30
    overlay_opacity: float = 0.6
    use_gpu: bool = True
    gpu_codec: str = "h264_nvenc"
    gpu_preset: str = "fast"
    crf: int = 23
    safe_start_margin: float = 1.0
    safe_end_margin: float = 1.0
    music_volume: float = 1
    fade_duration_clip: float = 0.3

# -----------------------------
# AI / OpenAI Settings
# -----------------------------
@dataclass
class AISettings:
    model: str = "gpt-4o"
    temperature: float = 0.5
    num_responses: int = 1
    api_key: str = os.getenv("OPENAI_API_KEY")

# -----------------------------
# File / Output Settings
# -----------------------------
@dataclass
class FileSettings:
    motivational_output: Path = DATA_GENERATED_DIR / "motivational_content.json"
    video_file: Path = ASSETS_DIR / "videos"
    music_file: Path = ASSETS_DIR / "musics"
    logo_file: Path = ASSETS_DIR / "logo" / "logo.png"
    generated_reel_file: Path = DATA_GENERATED_DIR / "reels"
    font: Path = ASSETS_DIR / "fonts" / "NotoSerifDisplay_Condensed-Medium.ttf"

# -----------------------------
# Global Settings Container
# -----------------------------
@dataclass
class Settings:
    base_dir: Path = BASE_DIR
    assets_dir: Path = ASSETS_DIR
    data_dir: Path = DATA_DIR
    log_level: int = LOG_LEVEL
    ai: AISettings = field(default_factory=AISettings)         # ✅ Use default_factory
    files: FileSettings = field(default_factory=FileSettings)  # ✅ Use default_factory
    video: VideoConfig = field(default_factory=VideoConfig)    # ✅ Use default_factory

# Singleton instance for use across the project
settings = Settings()
