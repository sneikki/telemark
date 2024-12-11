from fastapi import FastAPI
from lib.td_json import (
    TDJsonInterface as td_json, handle_log_messages, create_tdjson_interface)
from lib.td_client import create_client, send_query, execute_query, receive_result

TDJSON_LIBRARY_PATH = "/home/gattolina/git-repos/td/tdlib/lib/libtdjson.so"

create_tdjson_interface(TDJSON_LIBRARY_PATH)
td_json.td_set_log_message_callback(2, handle_log_messages)
execute_query({"@type": "setLogVerbosityLevel", "new_verbosity_level": 1})
# client_id = create_client()

send_query(client_id, {
        "@type": "getOption",
        "name": "version"})

app = FastAPI()


@app.get("/create")
def create():
    return {"client_id": create_client()}


@app.get("/")
def current_state():
    state = receive_result()

    return {"current_state":  state}


# def show_result_object(result_object):
#     if result_object.is_error():
#         print(f"[error] {result_object.payload["code"]}: {
#             result_object.payload["message"]}")

#     elif result_object.is_ok():
#         print("[ok]")

#     elif result_object.is_update():
#         print(f"[update]: {result_object.type}")
