from graphpy.tasks.abstract.task import Task
from graphpy.finished_signal import FinishedSignal

import requests
import random

from typing import Union, Type, Any, Optional


class WordGeneratorTask(Task):
    def __init__(self, max_words: int = 5) -> None:
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

        response = requests.get(word_site)
        self.words = response.content.decode("utf-8").splitlines()
        self.words_left = max_words

    def evaluate(self, data: None, sender: Task) -> Union[str, FinishedSignal]:
        if self.words_left == 0:
            return FinishedSignal()
        self.words_left -= 1
        return random.choice(self.words)

    @staticmethod
    def get_input_types() -> list[Type[Any]]:
        return []

    @staticmethod
    def get_output_type() -> Optional[Type[Any]]:
        return str
