from piracyshield_component.log.logger import Logger
from piracyshield_component.utils.time import Time

from abc import ABC, abstractmethod
from rq import get_current_job

class BaseTask(ABC):

    created_at = None

    def __init__(self):
        self.logger = Logger('tasks')

        self.created_at = Time.now_iso8601()

        self.job = get_current_job()

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def before_run(self, *args, **kwargs):
        pass

    @abstractmethod
    def after_run(self, *args, **kwargs):
        pass

    @abstractmethod
    def on_failure(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        try:
            self.before_run(*args, **kwargs)

            self.logger.debug('Task {} started with args: {}, kwargs: {}'.format(self.__class__.__name__, args, kwargs))

            result = self.run(*args, **kwargs)

            self.logger.debug('Task {} completed successfully with result: {}'.format(
                self.__class__.__name__, result))

            self.after_run(*args, **kwargs)

            return result

        except Exception as e:
            self.logger.error('Task {} failed with error: {}'.format(self.__class__.__name__, str(e)))

            self.on_failure(*args, **kwargs)

            self.job.meta['error'] = str(e)

            self.job.save()

            self.job.refresh()

            raise e

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)
