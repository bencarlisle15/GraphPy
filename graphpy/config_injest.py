from graphpy.tasks.abstract.task import Task
from graphpy.tasks.abstract.initiator import Initiator
from typing import Any, Type, Callable

import importlib
import uuid


def get_class_for_name(name: str) -> Type[Task]:
    split_index = name.rindex(".")
    module_name = name[:split_index]
    class_name = name[split_index + 1 :]
    module = importlib.import_module(module_name)
    clazz = getattr(module, class_name)
    if not isinstance(clazz, type) or not issubclass(clazz, Task):
        raise Exception("Class: %s is not a Task" % name)
    return clazz


def create_node(node_config: dict[str, Any]) -> tuple[str, Task]:
    task_id = node_config.pop("id")
    task_name = node_config.pop("name")
    task_class = get_class_for_name(task_name)
    task = task_class(**node_config)
    return task_id, task


def is_compatible(from_node: Task, to_node: Task) -> bool:
    from_node_output = type(from_node).get_output_type()
    to_node_inputs = type(to_node).get_input_types()
    if from_node_output is None or len(to_node_inputs) == 0:
        return False
    return any(
        [
            issubclass(from_node_output, to_node_input)
            for to_node_input in to_node_inputs
        ]
    )


def create_nodes(
    nodes_config: list[dict[str, Any]]
) -> tuple[dict[str, Task], list[str]]:
    nodes = {}
    initiator_nodes = []
    for node_config in nodes_config:
        task_id, task = create_node(node_config)
        if task_id in nodes:
            raise Exception("Task id: %s already exists!" % task_id)
        elif task is None:
            raise Exception("Task cannot be None")
        elif len(task_id) == 0:
            raise Exception("Task id cannot be empty")
        elif isinstance(task, Initiator):
            raise Exception("Cannot create an initiator")
        elif not isinstance(task, Task):
            raise Exception("Task must be a task")
        elif len(type(task).get_input_types()) == 0:
            initiator_nodes.append(task_id)
        nodes[task_id] = task
    return nodes, initiator_nodes


def create_links(
    nodes: dict[str, Task], links_config: list[dict[str, str]]
) -> dict[str, list[Task]]:
    links: dict[str, list[Task]] = {}
    for link in links_config:
        from_id = link["from"]
        to_id = link["to"]

        from_node = nodes[from_id]
        to_node = nodes[to_id]

        if not is_compatible(from_node, to_node):
            raise Exception("Node: %s cannot point to %s" % (from_id, to_id))
        elif from_id not in links:
            links[from_id] = []
        links[from_id].append(to_node)
    return links


def set_children(nodes: dict[str, Task], links: dict[str, list[Task]]) -> None:
    for link_id in links:
        nodes[link_id].set_children(links[link_id])


def link_initatior(
    nodes: dict[str, Task], initiator_node_ids: list[str], links: dict[str, list[Task]]
) -> Task:
    initiator = Initiator()
    nodes[""] = initiator

    for node_id in initiator_node_ids:
        if node_id not in links:
            links[node_id] = []
        links[node_id].append(initiator)

    return initiator


def config_injest(config: Any) -> tuple[Task, list[Task], list[Task]]:
    nodes, initiator_node_ids = create_nodes(config["nodes"])
    links = create_links(nodes, config["links"])
    initiator = link_initatior(nodes, initiator_node_ids, links)
    set_children(nodes, links)

    initiator_nodes = [nodes[node_id] for node_id in initiator_node_ids]

    return initiator, initiator_nodes, list(nodes.values())
