import log12

log = log12.logger("my-name")

with log.event("Log something") as event:
    event.bind(hello="World", test="something")
    
    with event.child("Subevent") as chev:
        chev.bind(foo="bar")
        chev.error("Catastrophe")

    with event.child("Subevent 2") as chev2:
        chev2.bind(bar="foo")

    with event.child("Subevent 3") as ev:
        ev.bind(bar="foo")

    with event.child("Subevent 4") as ev:
        ev.bind(bar="foo")