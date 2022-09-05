from typing import Any

import json
from graphpy import config_injest, executor
import argparse


def graphpy_main(config: Any) -> None:
    initiator, initiator_nodes, nodes = config_injest.config_injest(config)
    executor.execute(initiator, initiator_nodes, nodes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GraphPy")

    parser.add_argument(
        "--config", type=str, help="Config to import", default="configs/default.json"
    )

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)
    graphpy_main(config)
