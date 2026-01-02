from pathlib import Path
import logging
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
import datetime
from app.utils.logger import SingletonLogger

load_dotenv()

# Base Directories
BASE_DIR: Path = Path(__file__).resolve().parents[2]
YOUTUBE_SECRET_DIR: Path = BASE_DIR / "youtube_secret"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR: Path = BASE_DIR / "assets"
LOGOS_DIR: Path = ASSETS_DIR / "logo"
MUSICS_DIR: Path = ASSETS_DIR / "musics"
VIDEOS_DIR: Path = ASSETS_DIR / "videos"

DATA_DIR: Path = BASE_DIR / "data"
DATA_GENERATED_DIR: Path = DATA_DIR / "generated"
REELS_DIR: Path = DATA_GENERATED_DIR / "reels"
UPLOADED_REELS_DIR: Path = DATA_DIR / "uploaded_reels"

directories = [
    LOGS_DIR,
    YOUTUBE_SECRET_DIR,
    ASSETS_DIR,
    LOGOS_DIR,
    MUSICS_DIR,
    VIDEOS_DIR,
    DATA_DIR,
    DATA_GENERATED_DIR,
    REELS_DIR,
    UPLOADED_REELS_DIR
]

# Logging Configuration
LOG_LEVEL = logging.DEBUG if os.getenv("ENV") == "development" else logging.INFO
log_dir = Path("logs")
logger = SingletonLogger(name=__name__, log_level=LOG_LEVEL, log_dir=log_dir).get_logger()

def create_project_structure(dir_list: list[Path]):
    for directory in dir_list:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Verified directory: {directory.relative_to(BASE_DIR)}")

# Execute the setup
create_project_structure(directories)

# YouTube / Upload Settings
@dataclass
class YouTubeConfig:
    # API & Authentication
    scopes: list[str] = field(default_factory=lambda: ["https://www.googleapis.com/auth/youtube.upload"])
    client_secrets_file: Path = BASE_DIR / "youtube_secret/secret.json"
    token_file: Path = BASE_DIR / "youtube_secret/token.pickle"

    # Video folder paths
    video_folder: Path = REELS_DIR
    uploaded_reels_path: Path = UPLOADED_REELS_DIR
    last_upload_file: Path = DATA_DIR / "last_upload_time.txt"

    # Scheduling times
    publish_times_sri_lanka: list = field(
        default_factory=lambda: [
            datetime.time(6, 0),
            datetime.time(13, 0),
            datetime.time(18, 0),
            datetime.time(21, 0)
        ]
    )
    timezone_offset: float = 5.5  # Sri Lanka UTC+5:30

    # Default tags
    default_tags: list[str] = field(
        default_factory=lambda: ["shorts", "youtube shorts", "motivation", "luxury lifestyle", "inspiration"]
    )

# Video Generation Settings
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

# AI / OpenAI Settings
@dataclass
class AISettings:
    model: str = "gpt-4o"
    temperature: float = 0.5
    num_responses: int = 1
    api_key: str = os.getenv("OPENAI_API_KEY")

# File Output Settings
@dataclass
class FileSettings:
    motivational_output: Path = DATA_GENERATED_DIR / "motivational_content.json"
    video_file: Path = ASSETS_DIR / "videos"
    music_file: Path = ASSETS_DIR / "musics"
    logo_file: Path = ASSETS_DIR / "logo" / "logo.png"
    generated_reel_file: Path = DATA_GENERATED_DIR / "reels"
    font: Path = ASSETS_DIR / "fonts" / "NotoSerifDisplay_Condensed-Medium.ttf"

# Global Settings Container
@dataclass
class Settings:
    base_dir: Path = BASE_DIR
    assets_dir: Path = ASSETS_DIR
    data_dir: Path = DATA_DIR
    log_level: int = LOG_LEVEL
    ai: AISettings = field(default_factory=AISettings)         
    files: FileSettings = field(default_factory=FileSettings)
    video: VideoConfig = field(default_factory=VideoConfig) 
    youtube: YouTubeConfig = field(default_factory=YouTubeConfig)

# Singleton instance for use across the project
settings = Settings()
