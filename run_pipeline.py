import argparse
from pathlib import Path
from app.config.settings import settings
from app.ai_workflow.generator import ContentGenerator
from app.media.generator import VideoGenerator
from app.shorts_uploader.youtube_scheduler import YouTubeScheduler
from app.utils.logger import SingletonLogger
import logging


log_dir = Path("logs")
logger = SingletonLogger(name=__name__, log_level=settings.log_level, log_dir=log_dir).get_logger()


def run_ai_content_generation(logger, response_count):
    """
    Generate motivational content using AI.
    """
    logger.info("Starting AI content generation...")
    generator = ContentGenerator(logger=logger)
    generator.generate_batch(response_count)
    logger.info("AI content generation completed.")


def run_video_generation(logger):
    """
    Generate videos from AI-generated content.
    """
    logger.info("Starting video generation...")
    generator = VideoGenerator(logger=logger)
    generator.generate_batch()
    logger.info("Video generation completed.")


def run_youtube_scheduler(logger):
    """
    Schedule and upload videos to YouTube.
    """
    logger.info("Starting YouTube scheduling workflow...")
    scheduler = YouTubeScheduler(logger=logger)
    scheduler.run()
    logger.info("YouTube scheduling workflow completed.")


def main(video_count):
    """
    Application entry point.
    """
    logger.info("Application started")

    try:
        run_ai_content_generation(logger, video_count)
        run_video_generation(logger)
        run_youtube_scheduler(logger)
        logger.info("Application finished successfully.")
    except Exception:
        logger.exception("Application terminated due to an unexpected error.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AI content and video generator.")
    parser.add_argument(
        "--video-count",
        type=int,
        default=1,
        help="Number of videos to generate (default: 1)"
    )
    args = parser.parse_args()
    main(args.video_count)
