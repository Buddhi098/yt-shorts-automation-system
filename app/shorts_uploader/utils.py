import os
import pickle
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.config.settings import settings

SCOPES = settings.youtube.scopes
CLIENT_SECRETS_FILE = settings.youtube.client_secrets_file
TOKEN_FILE = settings.youtube.token_file

def get_authenticated_service():
    """Authenticate and return a YouTube API client."""
    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if not CLIENT_SECRETS_FILE.exists():
            raise FileNotFoundError(f"Client secrets not found at {CLIENT_SECRETS_FILE}")
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def read_last_upload_time(file_path):
    if file_path.exists():
        with open(file_path, "r") as f:
            ts = f.read().strip()
            if ts:
                return datetime.datetime.fromisoformat(ts)
    return None

def save_last_upload_time(file_path, dt):
    with open(file_path, "w") as f:
        f.write(dt.isoformat())
