import time, uuid, json, nanoid
from datetime import datetime, timezone

class Event:

    def __init__(self, logger : str, op : str, globals : dict, **kwargs):
        self.timestamp_ns = time.time_ns()
        self.logged = False
        self.data = dict(kwargs)
        self.globals = globals
        self.children = []
        self.data.update({
            'log_logger': logger,
            'log_start_ns': time.time_ns(),
            'log_start': datetime.now(timezone.utc).isoformat(),
            'log_event': event,
            'log_id': nanoid.generate()
        }
        self.data.update(kwargs)
        self.children = []

    def id(self) -> str:
        return self.data['log_id']

    def child(self, event : str, **kwargs):
        if not self.logged:
            ev = Event(self.data['log_logger'], event, self.globals, log_parent_id=self.data['log_id'], **kwargs)
            self.children.append(ev)
            return ev
        return None

    def children(self) -> int:
        return len(self.children)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type:
            self.error("Failed", log_exception=f"{exception_type} ({exception_value})")
        self.info("Completed")

    def update(self, **kwargs):
        if not self.logged:
            self.data.update(kwargs)

    def log(self, result : str, level : str, **kwargs):        
        if not self.logged:
            for child_event in self.children:
                child_event.log("Terminated by parent event", level)
            
            self.data.update(self.globals)
            self.update(log_result=result, log_level=level, **kwargs)
            self.update(log_duration_ns=time.time_ns() - self.timestamp_ns)
            print(json.dumps(self.data))
            self.logged = True

    def debug(self, result : str, **kwargs):
        self.log(result, "debug", **kwargs)

    def info(self, result : str, **kwargs):
        self.log(result, "info", **kwargs)

    def warn(self, result : str, **kwargs):
        self.log(result, "warn", **kwargs)

    def error(self, result : str, **kwargs):
        self.log(result, "error", **kwargs)

    def fatal(self, result : str, **kwargs):
        self.log(result, "fatal", **kwargs)

class EventStream:

    def __init__(self, name : str, **kwargs):
        self.logger = name
        self.globals = dict(kwargs)

    def event(self, op : str, **kwargs):
        return Event(self.logger, op, self.globals, **kwargs)

def logging(name : str, **kwargs):
    return EventStream(name, **kwargs)
