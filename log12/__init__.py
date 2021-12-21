import time, uuid, json, string
from datetime import datetime, timezone
from secrets import choice

class Event:

    def __init__(self, logger, event, **kwargs):
        self.logged = False
        self.data = {
            'log_logger': logger,
            'log_start_ns': time.time_ns(),
            'log_start': datetime.now(timezone.utc).isoformat(),
            'log_event': event,
            'log_id': uuid.uuid4().hex
        }
        self.data.update(kwargs)
        self.children = []

    def id(self):
        return self.data['log_id']

    def child(self, event, **kwargs):
        ev = Event(self.data['log_logger'], event, log_parent_id=self.data['log_id'], **kwargs)
        self.children.append(ev)
        return ev

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type:
            self.error("Failed", log_exception=f"{exception_type} ({exception_value})")
        self.info("Completed")

    def bind(self, **kwargs):
        if not self.logged:
            self.data.update(kwargs)

    def log(self, result, level, **kwargs):        
        if not self.logged:
            for child_event in self.children:
                child_event.log("Log triggered by parent event", level)
            
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
