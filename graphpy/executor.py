from graphpy.tasks.abstract.task import Task

from graphpy.pool.pool import Pool

import time


def execute(initiator: Task, initiator_nodes: list[Task], nodes: list[Task]) -> None:
    pool = Pool(len(nodes))
    pool.start()
    for node in initiator_nodes:
        pool.add_task(None, initiator, node)
    pool.wait_until_finished()
    print("Done with execution")
    pool.close()
