from datetime import timedelta

class Config:
    table = "_lonny_pg_guard"
    default_name = "_default"
    default_duration = timedelta(minutes = 20)
    old_lock_duration = timedelta(days = 30)