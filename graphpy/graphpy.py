from typing import Any

from graphpy.config_injest import config_injest
from graphpy.executor import execute


class GraphPy:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def start(self) -> None:
        initiator, initiator_nodes, nodes = config_injest(self.config)
        execute(initiator, initiator_nodes, nodes)
