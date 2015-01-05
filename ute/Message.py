import json

class Message:
    def __init__(self, action, id = None, type = None, desc = None, open = None, close = None):
        if action not in ["new", "close"]:
            raise Exception("Invalid action")

        self.action = action
        self.id = id
        self.type = type
        self.desc = desc
        self.open = open
        self.close = close

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(c, js):
        obj = json.loads(js)
        return Message(
            action = obj['action'],
            id = obj['id'],
            type = obj['type'],
            desc = obj['desc'],
            open = obj['open'],
            close = obj['close'])


