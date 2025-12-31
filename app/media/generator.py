import random
import logging
from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
from app.config.settings import settings
from .processor import VideoProcessor
from .utils import MediaUtils

class VideoGenerator:
    def __init__(self, logger):
        """
        Main class for generating motivational videos.
        Handles GPU detection, clip processing, and batch generation.
        """
        self.config = settings.video
        self.processor = VideoProcessor(logger)
        self.utils = MediaUtils(logger)
        self.gpu_available = self.utils.check_gpu_support()
        self.logger = logger
        if not self.gpu_available:
            self.config.use_gpu = False
            self.logger.warning("GPU not available, using CPU for encoding.")

    def generate_video(
        self,
        quotes: list[str],
        output_index: int,
        videos_folder: str = settings.files.video_file,
        music_folder: str = settings.files.music_file,
        logo_path: str = settings.files.logo_file,
        output_folder: str = settings.files.generated_reel_file,
    ) -> bool:
        """
        Generate a single motivational video.
        """
        Path(output_folder).mkdir(exist_ok=True)

        # 1️⃣ Select and trim video clips
        clips = self.processor.select_random_videos(videos_folder, len(quotes))
        trimmed_clips = [self.processor.trim_random_clip(c) for c in clips]

        # 2️⃣ Merge clips with motivational text
        color_set = random.choice(self.processor.color_sets)
        merged_clip = self.processor.merge_videos_with_text(trimmed_clips, quotes, color_set)

        if not merged_clip:
            self.logger.error("Failed to merge video clips.")
            self.utils.cleanup_clips(clips + trimmed_clips)
            return False

        # 3️⃣ Generate hook clip and prepend
        hook_clip = self.processor.generate_hook_clip(color_set)
        final_clip = concatenate_videoclips([hook_clip, merged_clip], method="compose") if hook_clip else merged_clip

        # 4️⃣ Add background music
        audio_clip = self.processor.get_random_music(music_folder)
        if audio_clip:
            final_clip = self.processor.add_music_to_video(final_clip, audio_clip)

        # 5️⃣ Add logo overlay
        final_clip = self.processor.add_logo_to_video(final_clip, logo_path)

        # 6️⃣ Write output video
        output_path = Path(output_folder) / f"reel_{output_index}.mp4"
        try:
            final_clip.write_videofile(str(output_path), fps=self.config.fps)
        except Exception as e:
            self.logger.error(f"Error writing video {output_index}: {e}")
            self.utils.cleanup_clips([final_clip] + trimmed_clips + clips)
            if audio_clip:
                audio_clip.close()
            return False

        # 7️⃣ Cleanup resources
        self.utils.cleanup_clips([final_clip] + trimmed_clips + clips)
        if audio_clip:
            audio_clip.close()

        self.logger.info(f"✅ Video {output_index} generated successfully.")
        return True

    def generate_batch(self):
        """
        Generate multiple motivational videos in a batch.
        """
        quotes_list = self.utils.load_quotes(settings.files.motivational_output)
        if not quotes_list:
            self.logger.error("No quotes found for video generation.")
            return 0
        count = len(quotes_list)

        successful = 0
        for i in range(count):
            quotes = quotes_list[i % len(quotes_list)]
            if self.generate_video(quotes, i + 1):
                successful += 1
            else:
                self.logger.warning(f"Failed to generate video {i + 1}.")

        self.logger.info(f"🎉 Batch generation complete: {successful}/{count} videos successful.")
        return successful
