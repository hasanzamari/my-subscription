import heapq


class PriorityManager:

    def __init__(self, limit=1000):

        self.limit = limit
        self.heap = []

    def add(self, score, config):

        heapq.heappush(
            self.heap,
            (score, config)
        )

        if len(self.heap) > self.limit:
            heapq.heappop(self.heap)

    def items(self):

        return sorted(
            self.heap,
            reverse=True
        )
