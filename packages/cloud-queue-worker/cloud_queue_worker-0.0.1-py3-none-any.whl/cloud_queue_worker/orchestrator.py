import time
from datetime import datetime, timedelta
import signal
from multiprocessing import Queue
from typing import Dict
from .worker.worker import ReadWorker, ExecutorWorker
from .errors import ConfigError
from .utils import get_client


class Orchestrator:
    def __init__(self, queue_mapping: Dict[str, str], concurrency: int, cloud_provider_config: Dict[str, str]) -> None:
        self.cloud_provider_config = cloud_provider_config
        self.queue_mapping = self._build_internal_mapping(queue_mapping)
        self.concurrency = concurrency
        self.internal_queue = Queue()
        self.read_workers = []
        self.executor_workers = []
        self._is_running = True
        self._initialize_workers()
        self._register_shutdown_signals()

    def _build_internal_mapping(self, queue_mapping):
        """"""
        client = get_client(self.cloud_provider_config)
        queue_urls = client.list_queues().get("QueueUrls", [])
        for key in queue_mapping:
            if key not in queue_urls:
                raise ConfigError("The queue url {} does not exist".format(key))

        return queue_mapping

    def _initialize_workers(self):
        for queue_url in self.queue_mapping:
            self.read_workers.append(
                ReadWorker(internal_queue=self.internal_queue, queue_url=queue_url, cloud_provider_config=self.cloud_provider_config)
            )
        for _ in range(self.concurrency):
            self.executor_workers.append(
                ExecutorWorker(
                    queue_mapping=self.queue_mapping,
                    internal_queue=self.internal_queue,
                    cloud_provider_config=self.cloud_provider_config,
                )
            )

    def run(self):
        for read_worker in self.read_workers:
            read_worker.start()

        for executor_worker in self.executor_workers:
            executor_worker.start()

        self._check_workers_statuses()

    def _stop(self):
        for read_worker in self.read_workers:
            read_worker.exit.set()

        for executor_worker in self.executor_workers:
            executor_worker.exit.set()

        queue_vacuum_start = datetime.now()
        while not self.internal_queue.empty() or datetime.now() - queue_vacuum_start >= timedelta(seconds=30):
            self.internal_queue.close()

            for read_worker in self.read_workers:
                read_worker.join()

            for executor_worker in self.executor_workers:
                executor_worker.join()

    def _check_workers_statuses(self):
        while self._is_running:
            time.sleep(1)
            read_workers_to_remove = [read_worker for read_worker in self.read_workers if not read_worker.is_alive()]
            executor_workers_to_remove = [
                executor_worker for executor_worker in self.executor_workers if not executor_worker.is_alive()
            ]

            for read_worker_to_remove in read_workers_to_remove:
                self.read_workers.remove(read_worker_to_remove)
                new_read_worker = ReadWorker(self.internal_queue, self.cloud_provider_config, read_worker_to_remove.name)
                self.read_workers.append(new_read_worker)
                new_read_worker.start()

            for executor_worker_to_remove in executor_workers_to_remove:
                self.executor_workers.remove(executor_worker_to_remove)
                new_executor_worker = ExecutorWorker(self.queue_mapping, self.internal_queue, self.cloud_provider_config)
                self.executor_workers.append(new_executor_worker)
                new_executor_worker.start()

        self._stop()

    def _register_shutdown_signals(self):
        """
        docstring
        """
        for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGHUP]:
            signal.signal(sig, self._stop_orchestrator)

    def _stop_orchestrator(self, _signum, _frame):
        """
        docstring
        """
        print("a signal has been received. Stop orchestrator...")
        self._is_running = False
