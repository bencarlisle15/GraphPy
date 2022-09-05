from abc import ABC, abstractmethod

from graphpy.tasks.abstract.task import Task
from graphpy.pool.pool import Pool

from typing import (
    TypeVar,
    Generic,
    List,
    Union,
    get_args,
    get_origin,
    Optional,
    Any,
    Type,
)
from graphpy.finished_signal import FinishedSignal

AI = TypeVar("AI")
AO = TypeVar("AO")


class Aggregation(Task, ABC):
    @abstractmethod
    def store_data(self, data: Any, sender: Any) -> None:
        pass

    @abstractmethod
    def evaluate_aggregation(self, pool: Pool) -> None:
        pass

    def evaluate(self, data: Any, sender: Any) -> Union[Any, FinishedSignal]:
        pass

    def execute(self, pool: Any, data: Any, sender: Any) -> None:
        if isinstance(data, FinishedSignal):
            self.evaluate_aggregation(pool)
            for child in self.children:
                pool.add_task(data, child, sender)
            self.finish(pool)
            return
        self.store_data(data, sender)
