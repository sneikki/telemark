import os
from lib.td_json import TDJsonInterface as td_json, create_tdjson_interface, handle_log_messages
from lib.td_client import create_client, send_query, execute_query
from lib.td_event_loop import td_event_loop_thread


def _get_tdjson_library_path():
    library_path = os.getenv("TDJSON_LIBRARY_PATH")

    if library_path is None:
        raise RuntimeError("env: TDJSON_LIBRARY_PATH must point to tdjson object file.")
    else:
        return library_path


def _configure_logging():
    td_json.td_set_log_message_callback(2, handle_log_messages)
    execute_query({"@type": "setLogVerbosityLevel", "new_verbosity_level": 1})


def start_telegram_api_conversation():
    create_tdjson_interface(_get_tdjson_library_path())
    _configure_logging()
    create_client()
    query_tdlib_version()


def query_tdlib_version():
    query_id = send_query({"@type": "getOption", "name": "version"})

    if query_id:
        td_event_loop_thread.queue_query(
            query_id, lambda result_object: print(result_object.payload))
