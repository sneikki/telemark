from uuid import uuid4
import os
import json
from lib.td_json import (TDJsonInterface as td_json,
                         create_tdjson_interface,
                         handle_log_messages)

_client_id = None


def _get_tdjson_library_path():
    library_path = os.getenv("TDJSON_LIBRARY_PATH")

    if library_path is None:
        raise RuntimeError("env: TDJSON_LIBRARY_PATH must point to tdjson object file.")
    else:
        return library_path


def _configure_logging():
    td_json.td_set_log_message_callback(2, handle_log_messages)
    execute_query({
        "@type": "setLogVerbosityLevel",
        "new_verbosity_level": 1
    })


def start_api_conversation():
    create_tdjson_interface(_get_tdjson_library_path())
    _configure_logging()
    _create_client()
    _query_version()


def _query_version():
    send_query({"@type": "getOption", "name": "version"})


def _create_client():
    global _client_id
    _client_id = td_json.td_create_client_id()


def send_query(query):
    if _client_id is None:
        print("error: query sent while client id is undefined")
    else:
        query_id = str(uuid4())
        serialized_query = json.dumps(query | {"@extra": query_id})
        td_json.td_send(_client_id, serialized_query.encode("utf-8"))
        return query_id


def execute_query(query):
    return validate_json_query_result(
        td_json.td_execute(json.dumps(query).encode("utf-8")))


def receive_result(timeout=1.0):
    return validate_json_query_result(td_json.td_receive(timeout))


def validate_json_query_result(query_result):
    return (json.loads(query_result.decode("utf-8"))
            if query_result else query_result)
