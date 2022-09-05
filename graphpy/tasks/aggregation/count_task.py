from graphpy.tasks.abstract.aggregation import Aggregation

from typing import Any, Type, Optional

from graphpy.pool.pool import Pool


class CountTask(Aggregation):

    num_results = 0

    def store_data(self, data: str, sender: Any) -> None:
        self.num_results += len(data)

    def evaluate_aggregation(self, pool: Pool) -> None:
        for child in self.children:
            pool.add_task(self.num_results, child, self)

    @staticmethod
    def get_input_type() -> Optional[Type[Any]]:
        return str

    @staticmethod
    def get_output_type() -> Optional[Type[Any]]:
        return int
