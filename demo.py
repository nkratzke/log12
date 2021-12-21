import log12

log = log12.logger("test")

# Log events using the with clause
with log.event("Test") as event:
    event.bind(hello="World", test="something")
    # bind key value pairs to the event

    with event.child("Subevent 1 of Test") as ev:
        ev.bind(foo="bar")
        ev.error("Catastrophe")
        # Explicit call of log (here on error level)


    with event.child("Subevent 2 of Test") as ev:
        ev.bind(bar="foo")
        # Implicit call of ev.info("Success") (at block end)

    with event.child("Subevent 3 of Test") as ev:
        ev.bind(bar="foo")
        # Implicit call of ev.info("Success") (at block end)

# Log events withou with blocks is possible as well
# However, in this case you are responsible for the log event flow
ev = log.event("Another test", foo="bar")
ev.bind(bar="foo")
child = ev.child("Subevent of Another test", foo="bar")
child.info("Finished") # <= You are responsible to log child events before the parent event is logged
ev.info("Finished") # <= You are are responsible to log events explicity