import os
from threading import Thread
from collections import deque
from collections.abc import Callable
from typing import NamedTuple, cast
from lib.td_client import receive_result
from lib.result_object import ResultObject, build_result_object
from lib.authorization import update_authorization_state


type QueryAction = Callable[[ResultObject], None]

IS_VERBOSE = os.getenv("VERBOSE_MODE") == "verbose"


class QueuedQuery(NamedTuple):
    query_id: str
    query_action: QueryAction


class TDEventLoop(Thread):
    queued_queries: deque[QueuedQuery]

    def run(self):
        self.queued_queries = deque()

        while True:
            result_object = build_result_object(receive_result())

            if result_object is not None:
                if (result_object.type == "updateAuthorizationState"):
                    update_authorization_state(result_object)
                    if IS_VERBOSE:
                        print(f"[ AUTHORIZE ] RECV UPDATE_AUTHORIZATION_STATE RESULT_TYPE {result_object.type} RESULT_PAYLOAD {result_object.payload}")

                elif (not self._is_queue_empty() and
                        self._match_result_query_id(result_object)):
                    [query_id, query_action] = self.queued_queries.popleft()
                    query_action(cast(ResultObject, result_object))

                    if IS_VERBOSE:
                        print(f"[ TD_EVENT_LOOP ] MATCH QUERY_ID {query_id} RESULT_TYPE {result_object.type} RESULT_PAYLOAD {result_object.payload}")
                elif IS_VERBOSE:
                    print(f"[ TD_EVENT_LOOP ] RECV NOMATCH RESULT_TYPE {result_object.type} RESULT_PAYLOAD {result_object.payload}")

    def queue_query(self, query_id: str, query_action: QueryAction):
        self.queued_queries.append(QueuedQuery(query_id, query_action))

    def _match_result_query_id(self, result_object: ResultObject):
        if "@extra" in result_object.payload:
            result_query_id = result_object.payload["@extra"]
            queue_head = self.queued_queries[0]
            return (result_query_id == queue_head.query_id)
        else:
            return None

    def _is_queue_empty(self):
        return (len(self.queued_queries) == 0)


td_event_loop_thread = TDEventLoop()
td_event_loop_thread.daemon = True
td_event_loop_thread.start()
