import signal
from multiprocessing import Process, Event, Queue
from typing import Dict, List, Any, Optional
from queue import Empty
from abc import ABC, abstractmethod
import os
import importlib
from ..utils import get_client


class Worker(Process, ABC):
    def __init__(self, internal_queue: Queue, cloud_provider_config: Dict[str, str], *args, **kwargs) -> None:
        """
        Main abstract class used to create read/write workers.
        :param internal_queue: Internal queue used to pass data between workers.
        :param cloud_provider_config: cloud provider config dict used to get appropriate client.
        """
        super().__init__(*args, **kwargs)
        self.internal_queue = internal_queue
        self.cloud_provider_config = cloud_provider_config
        self.exit = Event()

    @abstractmethod
    def run(self):
        pass


class ReadWorker(Worker):
    def __init__(self, internal_queue: Queue, cloud_provider_config: Dict[str, str], queue_url: str) -> None:
        """
        Read worker class. His role is the fetch messages from cloud provider queues
        and send them to internal queue to be processed by executor's workers.
        :param internal_queue: Internal queue used to pass data between workers.
        :param cloud_provider_config: cloud provider config dict used to get appropriate client.
        :param queue_url: Queue's url related to the worker
        """
        super().__init__(internal_queue, cloud_provider_config)
        self._queue_url = queue_url
        self.name = queue_url

    def run(self) -> None:
        """
        Start ReadWorker
        """
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        client = get_client(self.cloud_provider_config)
        print("The read worker with pid {}".format(os.getpid()))
        while not self.exit.is_set():
            messages = self.fetch_messages(client)
            if messages:
                self.send_messages_to_executor(messages)
        print("a signal has been received to close the read worker with pid {}".format(os.getpid()))

    def fetch_messages(self, client) -> List[Any]:
        """
        Fetch messages from cloud provider queue.
        :param client: Cloud provider client used to fetch messages
        """
        print("fetch messages from read worker")
        return client.receive_message(
            QueueUrl=self._queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
            VisibilityTimeout=60,
            AttributeNames=["SentTimestamp"],
            MessageAttributeNames=["All"],
        ).get("Messages", [])

    def send_messages_to_executor(self, messages: List[Any]) -> None:
        """
        Wrap messages with internal required data and send them to FIFO multiprocessing queue.
        :param messages: A list of messages.
        """
        print("send messages to executor")
        for message in messages:
            internal_message = {"message": message, "queue_url": self._queue_url}
            self.internal_queue.put(internal_message)


class ExecutorWorker(Worker):
    def __init__(
        self, queue_mapping: Dict[str, str], internal_queue: Queue, cloud_provider_config: Dict[str, str]
    ) -> None:
        """
        :param queue_mapping: Dict used to make the relation between the cloud provider queue
        and the worker used to process data.
        :param internal_queue: Internal queue used to pass data between workers.
        :param cloud_provider_config: cloud provider config dict used to get appropriate client.
        """
        super().__init__(internal_queue, cloud_provider_config)
        self.queue_mapping = queue_mapping

    def run(self) -> None:
        """
        Start ExecutorWorker
        """
        print("The executor worker with pid {} has been started".format(os.getpid()))
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        client = get_client(self.cloud_provider_config)
        while not self.exit.is_set() or not self.internal_queue.empty():
            message = self.fetch_message()
            if message:
                self.handle_message(message)
                self.acknowledge(message, client)
        print("a signal has been received to close the executor worker with pid {}".format(os.getpid()))

    def fetch_message(self) -> Optional[Dict[str, Any]]:
        """
        Fetch message from internal queue.
        :returns: Dict if there are data to process else None.
        """
        try:
            return self.internal_queue.get(timeout=0.5)
        except Empty:
            return None

    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Execute the function related to the message.
        :param message: internal queue's message.
        :type message: dict
        """
        print("handle message from executor worker")
        handler_path = self.queue_mapping[message["queue_url"]]
        function_name = handler_path.split(".")[-1]
        function_path = ".".join(handler_path.split(".")[:-1])

        function_module = importlib.import_module(function_path)

        function = getattr(function_module, function_name)
        function(message["message"])

    def acknowledge(self, message: Dict[str, Any], client):
        """
        Acknowledge the message at the end of the function's execution.
        :param message: internal queue's message.
        :param client: Cloud provider's client.
        """
        print("acknowledge message")
        client.delete_message(QueueUrl=message["queue_url"], ReceiptHandle=message["message"]["ReceiptHandle"])
