from typing import Optional, Dict, Union
from .errors import ConfigError
from .orchestrator import Orchestrator


class CloudQueueWorker:
    def __init__(
        self,
        queue_mapping: Optional[Dict[str, str]] = None,
        concurrency: Optional[int] = None,
        cloud_provider_config: Optional[Dict[str, str]] = None,
    ) -> None:
        self.queue_mapping = queue_mapping
        self.concurrency = concurrency
        self.cloud_provider_config = cloud_provider_config

    def update_config(self, config: Optional[Dict[str, Union[str, int]]]) -> None:
        """
        Update CloudQueueWorker object after initialization using a dict.
        :param config: dict to use to update CloudQueueWorker object
        :type config: dict
        :return: None
        """
        for key, value in config.items():
            setattr(self, key, value)

    def run(self) -> None:
        """
        Method to start CloudQueueWorker
        :return: None
        """
        if self.queue_mapping is None:
            raise ConfigError("queue_mapping parameter is missing in the config")

        if self.concurrency is None:
            raise ConfigError("concurrency parameter is missing in the config")

        if self.cloud_provider_config is None:
            raise ConfigError("cloud_provider_config parameter is missing in the config. Valid values: aws, azure, gcp")

        orchestrator = Orchestrator(**self.__dict__)
        orchestrator.run()
