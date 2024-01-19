from piracyshield_component.log.logger import Logger

from piracyshield_service.task.service import TaskService

from abc import ABC, abstractmethod

class BaseService(ABC):

    task_service = None

    logger = None

    def __init__(self):
        self.logger = Logger('service')

        self.task_service = TaskService()

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Executes the service main task.
        """

        pass

    def _schedule_task(self, *args, **kwargs):
        """
        Schedule a specific task.
        """

        pass

    @abstractmethod
    def _validate_parameters(self, *args, **kwargs):
        """
        Validates parameters in input.
        """

        pass

    @abstractmethod
    def _prepare_configs(self):
        """
        Prepares the config files.
        """

        pass

    @abstractmethod
    def _prepare_modules(self):
        """
        Prepare additional components.
        """

        pass
