import datetime
from app.config.settings import settings

PUBLISH_TIMES_SRI_LANKA = settings.youtube.publish_times_sri_lanka
TIMEZONE_OFFSET = settings.youtube.timezone_offset

def get_next_publish_datetimes(video_count, last_time_utc=None):
    """
    Generate a list of next publish datetimes (UTC) for the given number of videos.
    Distribute videos over scheduled times across days if needed.
    """
    now_utc = datetime.datetime.utcnow()
    if last_time_utc:
        # Start from next day after last upload
        start_day = (last_time_utc + datetime.timedelta(hours=TIMEZONE_OFFSET)).date() + datetime.timedelta(days=1)
    else:
        start_day = (now_utc + datetime.timedelta(hours=TIMEZONE_OFFSET)).date()

    schedule = []
    day = start_day
    while len(schedule) < video_count:
        for t in PUBLISH_TIMES_SRI_LANKA:
            dt_slt = datetime.datetime.combine(day, t)
            dt_utc = dt_slt - datetime.timedelta(hours=TIMEZONE_OFFSET)
            if dt_utc > now_utc:
                schedule.append(dt_utc)
            if len(schedule) >= video_count:
                break
        day += datetime.timedelta(days=1)
    return schedule
