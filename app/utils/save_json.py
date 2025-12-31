import json
from pathlib import Path

def save_json(data, file_path):
    try:
        file_path = Path(file_path)  # ensure it's a Path object
        file_path.parent.mkdir(parents=True, exist_ok=True)  # create parent dirs if needed
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise RuntimeError(f"Failed to save JSON to {file_path}: {e}")
