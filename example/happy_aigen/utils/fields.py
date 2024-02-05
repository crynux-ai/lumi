from datetime import datetime


def current_timestamp_ms() -> int:
    return int(datetime.now().timestamp()*1000)
