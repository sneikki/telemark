import sys
from typing import Callable
from ctypes import CDLL as SharedLibrary, CFUNCTYPE, c_int, c_double, c_char_p


class TDJsonInterface(type):
    @staticmethod
    def td_create_client_id() -> int:
        ...

    @staticmethod
    def td_send(client_id: int, request: str | bytes) -> None:
        ...

    @staticmethod
    def td_receive(timeout: float) -> str:
        ...

    @staticmethod
    def td_execute(request: str | bytes) -> str:
        ...

    @staticmethod
    def td_set_log_message_callback(max_verbosity_level: int,
                                    callback: Callable) -> None:
        ...


LogMessageCallbackType = CFUNCTYPE(None, c_int, c_char_p)


_TDJSON_FUNCTION_PROTOTYPES = [
    ("td_create_client_id", [], c_int),
    ("td_send", [c_int, c_char_p], None),
    ("td_receive", [c_double], c_char_p),
    ("td_execute", [c_char_p], c_char_p),
    ("td_set_log_message_callback", [c_int, LogMessageCallbackType], None)
]


def _register_tdjson_function(func, arg_types, res_type):
    local_func = func
    local_func.argtypes = arg_types
    local_func.restype = res_type

    return local_func


def _load_tdjson_library(tdjson_library_path: str):
    try:
        tdjson_library = SharedLibrary(tdjson_library_path)
    except OSError:
        sys.exit("tdjson library was not found")

    return tdjson_library


@LogMessageCallbackType
def handle_log_messages(message):
    sys.exit("tdlib encountered a fatal error: %r" % message)


def create_tdjson_interface(tdjson_library_path: str):
    tdjson_library = _load_tdjson_library(tdjson_library_path)

    for func_name, arg_types, res_type in _TDJSON_FUNCTION_PROTOTYPES:
        setattr(TDJsonInterface, func_name, _register_tdjson_function(
            tdjson_library[func_name], arg_types, res_type))
