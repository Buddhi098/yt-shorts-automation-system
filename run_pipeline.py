from app.utils.logger import get_logger
from pathlib import Path
from app.config.settings import settings
from app.ai_workflow.generator import ContentGenerator
from app.media.generator import VideoGenerator


# Initialize logger
logger = get_logger(
    name=__name__,
    log_level=settings.log_level,
    log_dir=Path("logs"),
)

logger.info("Application started")

# Define ai workflow steps
quoets_generator = ContentGenerator(logger=logger)
results = quoets_generator.generate_batch(settings.ai.num_responses)

# Define video generation workflow steps
video_generator = VideoGenerator(logger=logger)
video_generator.generate_batch()
