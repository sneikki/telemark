from server import socket

_authentication_state = "unauthenticated"


@socket.on("authentication-request")
def authentication_request(sid):
    if _authentication_state == "unauthenticated":
        print("authentication-request")
    else:
        return
