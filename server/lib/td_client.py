import json
from lib.td_json import TDJsonInterface as td_json


def create_client():
    return td_json.td_create_client_id()


def send_query(client_id, query):
    td_json.td_send(client_id, json.dumps(query).encode("utf-8"))


def execute_query(query):
    return validate_json_query_result(
        td_json.td_execute(json.dumps(query).encode("utf-8")))


def receive_result():
    return validate_json_query_result(td_json.td_receive(0.1))


def validate_json_query_result(query_result):
    return (json.loads(query_result.decode("utf-8"))
            if query_result else query_result)
