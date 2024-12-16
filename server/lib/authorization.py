import os
from server.socket_connection import socket
from lib.td_client import send_query
from lib.result_object import ResultObject

_authorization_state = "unauthorized"


@socket.on("authorization-request")
def authorization_request(sid):
    if _authorization_state == "unauthorized":
        print("authorization-request")
    else:
        return


def _send_tdlib_parameters():
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    tdlib_database_directory = os.getenv("TDLIB_DATABASE_DIRECTORY")

    if api_id is None:
        raise RuntimeError("[ ENV ] TELEGRAM_API_ID must be set to a valid API ID.")

    if api_hash is None:
        raise RuntimeError("[ ENV ] TELEGRAM_API_HASH must be set to a valid API hash.")

    if tdlib_database_directory is None:
        raise RuntimeError("[ ENV ] TDLIB_DATABASE_DIRECTORY must be set.")

    send_query({
        "api_id": int(api_id),
        "api_hash": api_hash,
        "database_directory": tdlib_database_directory,
        "@type": "setTdlibParameters",
        "use_message_database": True,
        "use_secret_chats": False,
        "system_language_code": "en",
        "device_model": "desktop",
        "application_version": "1.0"
     })


def update_authorization_state(result_object: ResultObject):
    global _authorization_state

    update_type = (result_object.payload["authorization_state"]["@type"]
                   .lower().removeprefix("authorizationstate"))

    event_name = None

    match update_type:
        case "waittdlibparameters":
            _send_tdlib_parameters()
        case "waitphonenumber":
            event_name = "provide-phone-number"
        case "waitemailaddress":
            event_name = "provide-email-address"
        case "waitemailcode":
            event_name = "provide-email-code"
        case "waitcode":
            event_name = "provide-code"
        case "waitregistration":
            event_name = "provide-registration-data"
        case "waitpassword":
            event_name = "provide-password"
        case "ready":
            event_name = "authorization-completed"
            _authorization_state = "authorized"
        case "closed":  # :D
            event_name = "authorization-revoked"
            _authorization_state = "unauthorized"

    if event_name is not None:
        socket.emit(event_name)
