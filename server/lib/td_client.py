from uuid import uuid4
import json
from lib.td_json import TDJsonInterface as td_json

_client_id = None


def create_client():
    global _client_id
    _client_id = td_json.td_create_client_id()


def send_query(query):
    if _client_id is None:
        print("error: attempted to send query while client id is undefined")
    else:
        query_id = str(uuid4())
        serialized_query = json.dumps(query | {"@extra": query_id})
        td_json.td_send(_client_id, serialized_query.encode("utf-8"))
        return query_id


def execute_query(query):
    return validate_json_query_result(
        td_json.td_execute(json.dumps(query).encode("utf-8")))


def receive_result(timeout=1.0):
    query_result = td_json.td_receive(timeout)

    return (validate_json_query_result(query_result) if query_result
            else None)


def validate_json_query_result(query_result):
    return json.loads(query_result.decode("utf-8"))
