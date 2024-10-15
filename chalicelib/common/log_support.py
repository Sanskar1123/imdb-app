import json
from datetime import datetime


def console_log(message):
    log_json = {
        "message": message,
        "log_timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(json.dumps(log_json))
