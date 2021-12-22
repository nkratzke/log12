import time, uuid, json, log12
from datetime import datetime, timezone
from secrets import choice

class Event:

    def __init__(self, logger : str, op : str, globals : dict, **kwargs):
        self.timestamp_ns = time.time_ns()
        self.logged = False
        self.data = dict(kwargs)
        self.globals = globals
        self.children = []
        self.data.update({
            'log_logger': logger,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'log_operation': op,
            'log_id': uuid.uuid4().hex
        })

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

    def bind(self, **kwargs):
        if not self.logged:
            self.data.update(kwargs)

    def log(self, result, level, **kwargs):        
        if not self.logged:
            for child_event in self.children:
                child_event.log("Terminated by parent event", level)
            
            self.data.update(self.globals)
            self.bind(log_result=result, log_level=level, **kwargs)
            self.bind(log_duration_ns=time.time_ns() - self.timestamp_ns)
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

    def __init__(self, name : str, **kwargs):
        self.logger = name
        self.globals = dict(kwargs)

    def event(self, op : str, **kwargs):
        return Event(self.logger, op, self.globals, **kwargs)

def logger(name, **kwargs):
    return EventStream(name, **kwargs)
