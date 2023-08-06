from datetime import timedelta
class Config:
    table = "_lonny_pg_queue"
    default_name = "_default"
    default_retry_interval = timedelta(minutes = 5)