from collections import deque


class TaskQueue:

    def __init__(self):
        self.queue = deque()

    def add(self, item):
        self.queue.append(item)

    def get(self):

        if not self.queue:
            return None

        return self.queue.popleft()

    def size(self):
        return len(self.queue)
