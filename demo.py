import log12
import requests

# Creation of a log stream with name "test"
# Each event and child events of this stream gets k/v pairs 
# - general="value"
# - tag="foo"
# These stream-specific k/v pairs can be used to define
# selection criteria in analytical databases like elasticsearch.
#
log = log12.logging("test", general="value", tag="foo", service_mark="test")

# We can create an event in a log stream like this:

# Log events using the with clause
with log.event("Test", hello="World") as event:
    event.update(test="something")
    # adds event specific key value pairs to the event

    with event.child("Subevent 1 of Test") as ev:
        ev.update(foo="bar")
        ev.error("Catastrophe")
        # Explicit call of log (here on error level)

    with event.child("Subevent 2 of Test") as ev:
        ev.update(bar="foo")
        # Implicit call of ev.info("Success") (at block end)

    with event.child("Subevent 3 of Test") as ev:
        ev.update(bar="foo")
        # Implicit call of ev.info("Success") (at block end)

# To log events without with-blocks is possible as well.
ev = log.event("Another test", foo="bar")
ev.update(bar="foo")
child = ev.child("Subevent of Another test", foo="bar")
ev.info("Finished") # <= However, than you are are responsible to log events explicity

headers = {
    "foo": "bar",
    "log_x": "y",
    "log-trace-id": "just a test"
}

with log.event("Termination test", extract=headers) as ev:

    # Here is how to pass tracing information along remote calls
    with ev.child("Task 1") as event:
        response = requests.get("https://qr.mylab.th-luebeck.dev/route?url=https://google.com", headers=event.inject())
        event.update(length=len(response.text), status_code=response.status_code)

    with ev.child("Task 2"):
        ev.error("Stopped")
        # If we log the parent event, this will implicity
        # log open child events automatically.