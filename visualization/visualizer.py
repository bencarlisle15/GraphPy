import argparse
import json

from typing import Any

from neo4j import GraphDatabase, Session  # type: ignore

from graphpy.config_injest import get_class_for_name
from graphpy.tasks.abstract.aggregation import Aggregation


def create_node(session: Session, node_config: dict[str, Any]) -> None:
    node_class = get_class_for_name(node_config["name"])
    create_node = "MERGE (n:%s {id: $id, name: $name})" % (
        "Aggregation" if issubclass(node_class, Aggregation) else "Task"
    )
    session.run(create_node, **node_config)


def create_link(
    session: Session, nodes: list[dict[str, Any]], link_config: dict[str, Any]
) -> None:
    node_config = [
        node_config for node_config in nodes if node_config["id"] == link_config["from"]
    ][0]
    from_node_class = get_class_for_name(node_config["name"])
    link_type_class = from_node_class.get_output_type()
    link_type = link_type_class.__name__ if link_type_class is not None else "None"
    create_link = """MATCH
        (f),
        (t)
        WHERE (f:Task OR f:Aggregation) AND (t:Task OR t:Aggregation) and f.id = $from AND t.id = $to
        MERGE (f)-[r:SendsTo {type: $type}]->(t)"""
    link_config["type"] = link_type
    session.run(create_link, **link_config)


def visualize(config: dict[str, Any], uri: str, username: str, password: str) -> None:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        for node_config in config["nodes"]:
            create_node(session, node_config)
        for link_config in config["links"]:
            create_link(session, config["nodes"], link_config)
    driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize GraphPy Config")

    parser.add_argument(
        "--config",
        type=str,
        help="Config to visualize",
        default="../graphpy_examples/configs/default.json",
    )
    parser.add_argument(
        "--uri", type=str, help="Neo4j URI", default="bolt://localhost:7687"
    )
    parser.add_argument("--username", type=str, help="Neo4j username", default="neo4j")
    parser.add_argument(
        "--password", type=str, help="Neo4j password", default="password"
    )

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)
    visualize(config, args.uri, args.username, args.password)
