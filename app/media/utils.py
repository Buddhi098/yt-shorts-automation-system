import subprocess
import json
from typing import List

class MediaUtils:
    def __init__(self, logger):
        """
        Media utilities for GPU detection, clip cleanup, and loading quotes.
        
        Args:
            logger: A logging.Logger instance for logging messages.
        """
        self.logger = logger

    def check_gpu_support(self) -> bool:
        """Detect NVIDIA GPU with NVENC support."""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return False

            ffmpeg_check = subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True, timeout=10)
            return 'h264_nvenc' in ffmpeg_check.stdout
        except Exception as e:
            self.logger.warning(f"GPU detection error: {e}")
            return False

    def cleanup_clips(self, clips):
        """Close all video/audio clips to free resources."""
        for clip in clips:
            try:
                if hasattr(clip, 'close'):
                    clip.close()
            except Exception:
                continue

    def load_quotes(self, file_path: str) -> List[List[str]]:
        """Load quotes from a JSON file or fallback to sample quotes."""
        quotes_list = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    quotes = item.get("quotes", [])
                    if quotes:
                        quotes_list.append(quotes)
        except FileNotFoundError:
            self.logger.warning(f"{file_path} not found, using sample quotes.")
            
        return quotes_list
