from datetime import timedelta

class Config:
    table = "_lonny_pg_schedule"
    default_name = "_default"
    dead_event_duration = timedelta(days = 1)