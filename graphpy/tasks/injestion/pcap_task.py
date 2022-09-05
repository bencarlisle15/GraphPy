from graphpy.tasks.abstract.task import Task
from scapy.utils import rdpcap  # type: ignore
from scapy.packet import Packet  # type: ignore

from graphpy.finished_signal import FinishedSignal

from typing import Union, Type, Any, Optional


class PcapTask(Task):
    def __init__(self, pcap_file: str) -> None:
        self.packets = iter(rdpcap(pcap_file))

    def evaluate(self, data: None, sender: Task) -> Union[Packet, FinishedSignal]:
        try:
            return next(self.packets)
        except StopIteration:
            return FinishedSignal()

    @staticmethod
    def get_input_type() -> Optional[Type[Any]]:
        return None

    @staticmethod
    def get_output_type() -> Optional[Type[Any]]:
        return Packet  # type: ignore
