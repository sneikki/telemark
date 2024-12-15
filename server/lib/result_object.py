class ResultObject:
    type: str
    payload: dict

    def __init__(self, _type: str, payload: dict):
        self.type = _type
        self.payload = payload

    def __str__(self):
        if self.is_error():
            return f"[ ERROR ] <code: {self.payload["code"]}> <message: {self.payload["message"]}>"

        elif self.is_ok():
            return "[ OK ]"

        elif self.is_update():
            return f"[ UPDATE ] <type: {self.type}> <name: {self.name}>"

        else:
            return f"ResultObject: unrecognized result type: {self.type} {self.payload}"

    def is_update(self):
        return self.type.startswith("update")

    def is_ok(self):
        return (self.type == "ok")

    def is_error(self):
        return (self.type == "error")

    @property
    def name(self):
        return (self.payload["name"]
                if "name" in self.payload
                else None)


def parse_result_data(result_data: dict | None):
    print(result_data)
    if result_data is None:
        return
    else:
        result_type = result_data["@type"]
        del result_data["@type"]

        return ResultObject(result_type, result_data)
