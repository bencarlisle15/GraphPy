from typing import Callable, Any

from queue import Queue
from graphpy.tasks.abstract.task import Task
from graphpy.pool.worker import Worker

from threading import Semaphore


class Pool:
    def __init__(self, num_nodes: int, max_workers: int = 20) -> None:
        self.workers = []
        self.queue: Queue[tuple[Any, Task, Task]] = Queue()
        self.num_running = Semaphore(0)
        self.num_nodes = num_nodes
        for _ in range(max_workers):
            self.workers.append(Worker(self))

    def start(self) -> None:
        for worker in self.workers:
            worker.start()

    # todo types
    def add_task(self, data: Any, task: Task, sender: Task) -> None:
        self.queue.put((data, task, sender))

    def close(self) -> None:
        for worker in self.workers:
            worker.close()
            worker.join()

    def add_finished(self) -> None:
        self.num_running.release()

    def wait_until_finished(self) -> None:
        # not counting initatior
        for _ in range(self.num_nodes - 1):
            self.num_running.acquire()
