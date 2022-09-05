import argparse
import json

from graphpy.graphpy import GraphPy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GraphPy")

    parser.add_argument(
        "--config", type=str, help="Config to import", default="configs/default.json"
    )

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)
    GraphPy(config).start()
