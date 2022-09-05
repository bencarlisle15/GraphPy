from graphpy.tasks.abstract.task import Task

from graphpy.finished_signal import FinishedSignal

from typing import Union, Any, Type, Optional


class PrintTask(Task):
    def evaluate(self, data: str, sender: Task) -> Union[None, FinishedSignal]:
        print(data)
        return None

    @staticmethod
    def get_input_types() -> list[Type[Any]]:
        return [object]

    @staticmethod
    def get_output_type() -> Optional[Type[Any]]:
        return None
