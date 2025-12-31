import os
import datetime
from pathlib import Path
from typing import Optional, List

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import logging


class YouTubeUploader:
    """
    Handles scheduling uploads to YouTube using the Data API.
    """

    def __init__(
        self,
        youtube_client,
        video_folder: Path,
        logger: logging.Logger,
    ):
        self.youtube = youtube_client
        self.video_folder = Path(video_folder)
        self.logger = logger

    def schedule_upload(
        self,
        video_file: str,
        title: str,
        description: str,
        publish_time: datetime.datetime,
        tags: Optional[List[str]] = None,
    ):
        """
        Schedule a video upload at a given UTC datetime.
        """
        tags = tags or []

        if publish_time <= datetime.datetime.utcnow():
            self.logger.warning(
                "Skipping upload for %s: publish time %s is in the past",
                video_file,
                publish_time,
            )
            return None

        publish_time_iso = publish_time.isoformat().replace("+00:00", "Z")

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_time_iso,
                "selfDeclaredMadeForKids": False,
            },
        }

        full_video_path = self.video_folder / video_file
        if not full_video_path.exists():
            self.logger.error("Video file not found: %s", full_video_path)
            return None

        try:
            self.logger.info("Starting upload: %s", video_file)

            media = MediaFileUpload(
                str(full_video_path),
                chunksize=-1,
                resumable=True,
            )

            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    self.logger.info(
                        "Upload progress for %s: %d%%",
                        video_file,
                        int(status.progress() * 100),
                    )

            self.logger.info(
                "Video '%s' successfully scheduled for %s",
                video_file,
                publish_time_iso,
            )
            return response

        except HttpError as e:
            self.logger.error(
                "YouTube API error while uploading %s (status %s): %s",
                video_file,
                e.resp.status,
                e.content,
            )
            return None

        except Exception:
            self.logger.exception(
                "Unexpected error occurred while uploading %s",
                video_file,
            )
            return None
