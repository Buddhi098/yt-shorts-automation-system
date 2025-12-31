import json
import shutil
import logging
from pathlib import Path
from typing import List

from app.config.settings import settings
from .utils import (
    get_authenticated_service,
    read_last_upload_time,
    save_last_upload_time,
)
from .scheduler import get_next_publish_datetimes
from .uploader import YouTubeUploader


class YouTubeScheduler:
    """
    Handles scheduling and uploading multiple videos to YouTube.
    Also performs post-upload cleanup.
    """

    def __init__(
        self,
        logger = None,
        content_file: Path = settings.files.motivational_output,
    ):
        self.content_file = content_file
        self.video_folder = settings.youtube.video_folder
        self.uploaded_reels_path = settings.youtube.uploaded_reels_path
        self.last_upload_file = settings.data_dir / "last_upload_time.txt"
        self.youtube_client = None
        self.videos: List[dict] = []

        # Logger fallback
        self.logger = logger

        # Ensure uploaded folder exists
        self.uploaded_reels_path.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Core workflow steps
    # -------------------------------------------------
    def load_videos(self):
        if not self.content_file.exists():
            self.logger.error("Content file not found: %s", self.content_file)
            raise FileNotFoundError(f"Content file not found: {self.content_file}")

        with open(self.content_file, "r", encoding="utf-8") as f:
            self.videos = json.load(f)

        if not self.videos:
            self.logger.error("No videos found in content file.")
            raise ValueError("No videos found to upload.")

        self.logger.info("Loaded %d videos for scheduling.", len(self.videos))

    def authenticate(self):
        self.logger.info("Authenticating YouTube client...")
        self.youtube_client = get_authenticated_service()
        self.logger.info("YouTube authentication successful.")

    def schedule_all_uploads(self):
        if self.youtube_client is None:
            self.logger.error("YouTube client not authenticated.")
            raise RuntimeError("YouTube client not authenticated.")

        uploader = YouTubeUploader(self.youtube_client, self.video_folder, logger=self.logger)
        last_upload_time = read_last_upload_time(self.last_upload_file)

        publish_schedule: List = get_next_publish_datetimes(
            len(self.videos), last_upload_time
        )

        self.logger.info("Scheduling %d videos.", len(self.videos))

        for i, video_info in enumerate(self.videos):
            video_file = f"reel_{video_info.get('id')}.mp4"
            full_path = self.video_folder / video_file

            if not full_path.exists():
                self.logger.warning("Skipping missing file: %s", video_file)
                continue

            title = video_info.get("video_title", f"My Reel {i + 1}")
            description = (
                f"{title}\n\n"
                f"{video_info.get('youtube_description', '')}\n\n"
                f"{', '.join(video_info.get('video_tags', []))}"
            )

            tags = settings.youtube.default_tags + video_info.get("video_tags", [])

            self.logger.info(
                "Scheduling video '%s' at %s",
                video_file,
                publish_schedule[i],
            )

            uploader.schedule_upload(
                video_file,
                title,
                description,
                publish_schedule[i],
                tags,
            )

        save_last_upload_time(self.last_upload_file, publish_schedule[-1])
        self.logger.info(
            "Last upload time saved: %s", publish_schedule[-1]
        )

    # -------------------------------------------------
    # 🧹 Post-upload cleanup
    # -------------------------------------------------
    def cleanup_after_upload(self):
        """
        Move generated reels to uploaded folder
        and delete motivational content JSON.
        """
        moved_files = 0

        for video_info in self.videos:
            video_file = f"reel_{video_info.get('id')}.mp4"
            src = self.video_folder / video_file
            dst = self.uploaded_reels_path / video_file

            if src.exists():
                shutil.move(str(src), str(dst))
                moved_files += 1
                self.logger.info("Moved video: %s", video_file)

        if self.content_file.exists():
            self.content_file.unlink()
            self.logger.info(
                "Deleted content file: %s", self.content_file
            )

        self.logger.info(
            "Cleanup complete: %d videos moved.", moved_files
        )

    # -------------------------------------------------
    # Entry point
    # -------------------------------------------------
    def run(self):
        """
        Execute the full scheduling workflow.
        """
        try:
            self.logger.info("Starting YouTube scheduling pipeline...")
            self.load_videos()
            self.authenticate()
            self.schedule_all_uploads()
            self.cleanup_after_upload()
            self.logger.info(
                "YouTube scheduling pipeline completed successfully."
            )
        except Exception as e:
            self.logger.exception(
                "Error occurred in YouTubeScheduler: %s", e
            )
