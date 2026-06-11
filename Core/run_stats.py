from datetime import datetime


class RunStats:

    def __init__(self):

        self.data = {

            "start": datetime.utcnow().isoformat(),

            "download": 0,

            "parse": 0,

            "validate": 0,

            "normalize": 0,

            "dedup": 0,

            "new": 0,

            "export": 0

        }

    def set(self, key, value):

        self.data[key] = value

    def get(self):

        return self.data
