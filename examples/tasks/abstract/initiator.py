from graphpy.tasks.abstract.task import Task
from graphpy.finished_signal import FinishedSignal

from typing import Any, Optional, Type

import time


class Initiator(Task):

    num_ended = 0

    def evaluate(self, data: str, sender: Task) -> None:
        pass

    def execute(self, pool: Any, data: Any, sender: Any) -> None:
        if isinstance(data, FinishedSignal):
            self.num_ended += 1
            return
        time.sleep(0.1)
        pool.add_task(None, sender, self)

    def get_num_ended(self) -> int:
        return self.num_ended

    @staticmethod
    def get_input_type() -> Optional[Type[Any]]:
        return None

    @staticmethod
    def get_output_type() -> Optional[Type[Any]]:
        return None
