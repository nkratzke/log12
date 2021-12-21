import log12

log = log12.logger("test")

with log.event("Test") as event:
    event.bind(hello="World", test="something")
    
    with event.child("Subevent 1 of Test") as ev:
        ev.bind(foo="bar")
        ev.error("Catastrophe")

    with event.child("Subevent 2 of Test") as ev:
        ev.bind(bar="foo")

    with event.child("Subevent 3 of Test") as ev:
        ev.bind(bar="foo")