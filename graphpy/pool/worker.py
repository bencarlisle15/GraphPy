from threading import Thread
from typing import Any
from queue import Queue, Empty

from graphpy.finished_signal import FinishedSignal


class Worker(Thread):

    is_open = True

    def __init__(self, pool: Any) -> None:
        super(Worker, self).__init__()
        self.pool = pool
        self.queue = pool.queue

    def run(self) -> None:
        while self.is_open:
            try:
                data, task, sender = self.queue.get(timeout=0)
            except Empty:
                continue
            # print(data,task,sender)
            task.execute(self.pool, data, sender)
            self.queue.task_done()

    def close(self) -> None:
        self.is_open = False
