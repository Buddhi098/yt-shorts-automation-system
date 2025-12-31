from pathlib import Path

from app.utils.logger import get_logger
from app.config.settings import settings
from app.ai_workflow.generator import ContentGenerator
from app.media.generator import VideoGenerator
from app.shorts_uploader.youtube_scheduler import YouTubeScheduler


def setup_logger():
    """
    Configure and return application logger.
    """
    return get_logger(
        name=__name__,
        log_level=settings.log_level,
        log_dir=Path("logs"),
    )


def run_ai_content_generation(logger, response_count=settings.ai.num_responses):
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


def main():
    """
    Application entry point.
    """
    logger = setup_logger()
    logger.info("Application started")

    video_count = 1

    try:
        run_ai_content_generation(logger , video_count)
        run_video_generation(logger)
        run_youtube_scheduler(logger)
        logger.info("Application finished successfully.")
    except Exception:
        logger.exception("Application terminated due to an unexpected error.")


if __name__ == "__main__":
    main()
