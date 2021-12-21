import time, uuid, json, string
from datetime import datetime, timezone
from secrets import choice

VERSION="0.0.1-b"

class Event:

    def __init__(self, logger, event, **kwargs):
        self.logged = False
        self.data = {
            'log_logger': logger,
            'log_start_ns': time.time_ns(),
            'log_start': datetime.now(timezone.utc).isoformat(),
            'log_event': event,
            'log_id': uuid.uuid4().hex,
            'log_child_events': []
        }
        self.data.update(kwargs)

    def id(self):
        return self.data['log_id']

    def child(self, event, **kwargs):
        ev = Event(self.data['log_logger'], event, log_parent_id=self.data['log_id'], **kwargs)
        self.data['log_child_events'].append(ev.id())
        return ev

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type:
            self.error("Failed", log_exception=f"{exception_type} ({exception_value})")
        self.info("Completed")

    def bind(self, **kwargs):
        self.data.update(kwargs)

    def log(self, result, level, **kwargs):
        if not self.logged:
            self.bind(log_result=result, log_level=level, log_end=datetime.now(timezone.utc).isoformat(), **kwargs)
            self.bind(log_duration_ns=time.time_ns() - self.data['log_start_ns'])
            print(json.dumps(self.data))
            self.logged = True

    def debug(self, result, **kwargs):
        self.log(result, "debug", **kwargs)

    def info(self, result, **kwargs):
        self.log(result, "info", **kwargs)

    def warn(self, result, **kwargs):
        self.log(result, "warn", **kwargs)

    def error(self, result, **kwargs):
        self.log(result, "error", **kwargs)

    def fatal(self, result, **kwargs):
        self.log(result, "fatal", **kwargs)

class EventStream:

    def __init__(self, name : str):
        self.logger = name

    def event(self, event : str, **kwargs):
        return Event(self.logger, event, **kwargs)

def logger(name):
    return EventStream(name)
