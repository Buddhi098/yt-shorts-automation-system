import random
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    ColorClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ImageClip,
    afx
)
from moviepy.video.fx import FadeIn, FadeOut
from pathlib import Path
from app.config.settings import settings


class VideoProcessor:
    """
    Handles video selection, processing, text overlays, music integration,
    branding, and final composition for short-form vertical videos.
    """

    def __init__(self, logger):
        """
        Initialize the video processor with configuration and logger.

        :param logger: Application logger instance
        """
        self.config = settings.video
        self.logger = logger

        # Predefined color combinations for text and strokes
        self.color_sets = [
            ("yellow", "white"),
            ("lime", "white"),
            ("orange", "white")
        ]

        # Hook phrases shown at the beginning of videos
        self.hook_phrases = [
            "99% are stuck for this one reason.",
            "Comfort is the killer of dreams.",
            "Change your circle or lose your future.",
            "Stop wanting it to finally get it."
        ]

    def resize_and_crop_vertical(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Resize and center-crop a video clip to match the target vertical resolution.

        Ensures the final output strictly matches target_width x target_height
        without distorting aspect ratio.

        :param clip: Input video clip
        :return: Resized and cropped video clip
        """
        current_aspect = clip.w / clip.h
        target_aspect = self.config.target_width / self.config.target_height

        # Resize based on aspect ratio comparison
        if current_aspect > target_aspect:
            clip_resized = clip.resized(height=self.config.target_height)
        else:
            clip_resized = clip.resized(width=self.config.target_width)

        # Center crop if dimensions exceed target
        if clip_resized.w != self.config.target_width or clip_resized.h != self.config.target_height:
            return clip_resized.cropped(
                x_center=clip_resized.w / 2,
                y_center=clip_resized.h / 2,
                width=self.config.target_width,
                height=self.config.target_height
            )

        return clip_resized

    def trim_random_clip(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Extract a random subclip of fixed duration while avoiding
        unsafe start and end margins.

        :param clip: Source video clip
        :return: Trimmed video clip
        """
        safe_duration = (
            clip.duration
            - self.config.safe_start_margin
            - self.config.safe_end_margin
        )
        clip_duration = self.config.video_duration

        if safe_duration <= clip_duration:
            start_time = 0.25
        else:
            max_start = clip.duration - clip_duration - self.config.safe_end_margin
            start_time = random.uniform(self.config.safe_start_margin, max_start)

        return clip.subclipped(start_time, start_time + clip_duration)

    def merge_videos_with_text(
        self,
        clips: list[VideoFileClip],
        sentences: list[str],
        color_set: tuple
    ) -> CompositeVideoClip:
        """
        Overlay centered text and dark background on each clip,
        apply fade-in/out effects, and concatenate all clips.

        :param clips: List of processed video clips
        :param sentences: Corresponding captions for each clip
        :param color_set: (stroke_color, text_color)
        :return: Final concatenated video
        """
        processed_clips = []
        font_path = settings.files.font

        # Fallback if font file is missing
        if not Path(font_path).exists():
            font_path = None

        fade_duration = self.config.fade_duration

        for clip, sentence in zip(clips, sentences):
            clip = self.resize_and_crop_vertical(clip).without_audio()

            # Text overlay
            txt_clip = (
                TextClip(
                    text=sentence,
                    font=font_path,
                    method="caption",
                    size=(900, None),
                    font_size=self.config.text_font_size,
                    color=color_set[1],
                    stroke_width=1,
                    stroke_color="grey",
                )
                .with_position("center")
                .with_duration(clip.duration)
            )

            # Dark overlay for readability
            dark_overlay = (
                ColorClip(clip.size, color=(0, 0, 0))
                .with_duration(clip.duration)
                .with_opacity(self.config.overlay_opacity)
            )

            # Compose scene
            scene = CompositeVideoClip([clip, dark_overlay, txt_clip])

            # Apply fade effects
            scene = scene.with_effects([
                FadeIn(duration=fade_duration),
                FadeOut(duration=fade_duration),
            ])

            processed_clips.append(scene)

        return concatenate_videoclips(processed_clips, method="compose")

    def generate_hook_clip(self, color_set: tuple) -> CompositeVideoClip:
        """
        Generate an intro hook clip with motivational text on a black background.

        :param color_set: Color set for hook text
        :return: Hook video clip
        """
        phrase = random.choice(self.hook_phrases)
        font_path = settings.files.font

        if not Path(font_path).exists():
            font_path = None

        txt_clip = (
            TextClip(
                text=phrase,
                font=font_path,
                method="caption",
                size=(800, 1000),
                font_size=self.config.hook_font_size,
                stroke_width=1,
                stroke_color=color_set[0],
                color=color_set[0],
            )
            .with_position("center")
            .with_duration(self.config.video_duration)
        )

        return CompositeVideoClip(
            [txt_clip],
            size=(self.config.target_width, self.config.target_height),
            bg_color=(0, 0, 0),
        )

    def select_random_videos(self, folder_path: str, count: int) -> list[VideoFileClip]:
        """
        Randomly select and load video files from a directory.

        :param folder_path: Directory containing videos
        :param count: Number of videos to select
        :return: List of loaded video clips
        """
        folder = Path(folder_path)
        video_extensions = (".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv")

        if not folder.exists():
            self.logger.error(f"Video folder not found: {folder_path}")
            return []

        video_files = [
            f for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in video_extensions
        ]

        if len(video_files) < count:
            self.logger.warning(
                f"Only {len(video_files)} videos available, requested {count}. Adjusting count."
            )
            count = len(video_files)

        selected_files = random.sample(video_files, count)
        clips = []

        for file in selected_files:
            try:
                clip = VideoFileClip(str(file))
                if clip.duration > 0 and clip.w > 0 and clip.h > 0:
                    clips.append(clip)
                    self.logger.info(
                        f"Loaded video: {file.name} ({clip.duration:.1f}s)"
                    )
                else:
                    clip.close()
            except Exception as e:
                self.logger.warning(f"Failed to load video {file.name}: {e}")

        return clips

    def get_random_music(self, folder_path: str) -> AudioFileClip | None:
        """
        Randomly select and load a background music track.

        :param folder_path: Directory containing audio files
        :return: Audio clip or None if unavailable
        """
        folder = Path(folder_path)
        audio_extensions = (".mp3", ".wav", ".m4a", ".aac", ".ogg")

        if not folder.exists():
            self.logger.warning(f"Music folder not found: {folder_path}")
            return None

        audio_files = [
            f for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in audio_extensions
        ]

        if not audio_files:
            self.logger.warning(f"No audio files found in {folder_path}")
            return None

        selected_file = random.choice(audio_files)

        try:
            audio_clip = AudioFileClip(str(selected_file))
            self.logger.info(
                f"Loaded audio: {selected_file.name} ({audio_clip.duration:.1f}s)"
            )
            return audio_clip
        except Exception as e:
            self.logger.warning(f"Failed to load audio {selected_file.name}: {e}")
            return None

    def add_music_to_video(self, video: VideoFileClip, audio: AudioFileClip) -> VideoFileClip:
        """
        Add background music to a video, looping and trimming as needed.

        :param video: Final video clip
        :param audio: Background audio clip
        :return: Video with background music
        """
        if audio.duration < video.duration:
            audio = afx.AudioLoop(duration=video.duration).apply(audio)

        audio = audio.subclipped(0, video.duration)
        audio = audio.with_volume_scaled(self.config.music_volume)

        return video.with_audio(audio)

    def add_logo_to_video(self, video: VideoFileClip, logo_path: str) -> VideoFileClip:
        """
        Overlay a logo image near the bottom center of the video.

        :param video: Base video clip
        :param logo_path: Path to logo image
        :return: Video with logo overlay
        """
        logo_file = Path(logo_path)

        if not logo_file.exists():
            self.logger.warning(f"Logo file not found: {logo_path}")
            return video

        bottom_padding = 250

        logo_clip = (
            ImageClip(str(logo_file))
            .with_fps(video.fps)
            .with_duration(video.duration)
            .resized(height=int(video.h * 0.1))
            .with_position(
                ("center", video.h - int(video.h * 0.1) - bottom_padding)
            )
        )

        return CompositeVideoClip([video, logo_clip])
