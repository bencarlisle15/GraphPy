from abc import ABC, abstractmethod
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


class Task(ABC):

    children: list[Any] = []
    is_finished = False

    def set_children(self, children: list[Any]) -> None:
        self.children = children

    @abstractmethod
    def evaluate(self, data: Any, sender: Any) -> Union[Any, FinishedSignal]:
        pass

    def execute(self, pool: Any, data: Any, sender: Any) -> None:
        if isinstance(data, FinishedSignal):
            self.finish(pool)
            return
        evaluated_data = self.evaluate(data, sender)
        for child in self.children:
            pool.add_task(evaluated_data, child, self)
        if isinstance(evaluated_data, FinishedSignal):
            self.finish(pool)

    @staticmethod
    @abstractmethod
    def get_input_type() -> Optional[Type[Any]]:
        pass

    @staticmethod
    @abstractmethod
    def get_output_type() -> Optional[Type[Any]]:
        pass

    def finish(self, pool: Any) -> None:
        if not self.is_finished:
            pool.add_finished()
        self.is_finished = True
