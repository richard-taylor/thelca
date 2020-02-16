from datetime import datetime, timezone

def current_time_UTC():
    return datetime.now(timezone.utc).isoformat()
