import time, json, nanoid, msgpack
from typing import Any
from datetime import datetime, timezone

TRACE_ID  = 'l3-trace-id'
EVENT_ID  = 'l3-event-id'
PARENT_ID = 'l3-parent-id'
LOGGER    = 'l3-logger'
START     = 'l3-start'
START_NS  = 'l3-start-ns'
OPERATION = 'l3-operation'
RESULT    = 'l3-result'
LEVEL     = 'l3-level'
DURATION  = 'l3-duration-ns'
EXCEPTION = 'l3-exception'

def normalize(d : dict[str, Any]):
    return { k.lower().replace("_", "-"): v for k, v in d.items() }

class Event:

    def __init__(self, logger : str, op : str, globals : dict, **kwargs):
        self.timestamp_ns = time.time_ns()
        self.logged = False
        self.data = dict(kwargs)
        self.globals = normalize(globals)
        self.children = []
        self.data.update({
            LOGGER:    logger,
            START_NS:  time.time_ns(),
            START:     datetime.now(timezone.utc).isoformat(),
            OPERATION: op,
            EVENT_ID:  nanoid.generate()
        })
        self.data.update(normalize(kwargs))
        self.children = []

    def id(self):
        return self.data[EVENT_ID]

    def trace_id(self):
        return self.data[TRACE_ID]

    def inject(self):
        return normalize({
            TRACE_ID: self.trace_id(),
            PARENT_ID: self.id()
        })

    def child(self, event : str, **kwargs):
        if not self.logged:
            kwargs.update(self.inject())
            ev = Event(self.data[LOGGER], 
                event, 
                self.globals,
                **normalize(kwargs)
            )
            self.children.append(ev)
            return ev
        return None

    def children(self) -> int:
        return len(self.children)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type:
            self.error("Failed", **{ EXCEPTION: f"{exception_type} ({exception_value})" })
        self.info("Completed")

    def update(self, **kwargs):
        if not self.logged:
            self.data.update(normalize(kwargs))

    def log(self, result : str, level : str, **kwargs):        
        if not self.logged:
            for child_event in self.children:
                child_event.log("Terminated by parent event", level)
            
            self.data.update(normalize(self.globals))
            self.update(**{ RESULT: result, LEVEL: level }, **kwargs)
            self.update(**{ DURATION: time.time_ns() - self.timestamp_ns})
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

    def event(self, op : str, extract: dict = {}, **kwargs):
        extract = { k.lower(): v for k, v in extract.items() }
        kwargs.update({
            PARENT_ID: extract.get(PARENT_ID, 'root'),               
            TRACE_ID: extract.get(TRACE_ID, nanoid.generate())                
        })
        return Event(self.logger, op, self.globals, **kwargs)

def logging(name : str, **kwargs):
    return EventStream(name, **kwargs)
