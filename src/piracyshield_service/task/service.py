from piracyshield_component.log.logger import Logger

from piracyshield_service.task.instance import TaskInstanceService

from datetime import timedelta

from rq.exceptions import InvalidJobOperation

class TaskService(TaskInstanceService):

    """
    Task management class.
    """

    logger = None

    def __init__(self):
        super().__init__()

        self.logger = Logger('service')

    def create(self, task_caller: callable, delay: int = 0, *args: list, **kwargs: dict) -> str:
        """
        Creates a task.
        Expects a caller function that calls a BaseTask extended class.

        :param task_caller: a function that calls the main task class.
        :param delay: seconds of delay before the task is executed.
        :param *args: arguments to pass to the task class.
        :param **kwargs: keyword arguments to pass to the task class.
        :return: the queue job id.
        """

        scheduled_time = timedelta(seconds = delay)

        job = self.queue.enqueue_in(
            scheduled_time,
            task_caller,
            *args,
            **kwargs
        )

        self.logger.info(f'Enqueued new task `{job.id}` to be started at `{scheduled_time}`')

        return job.id

    def remove(self, job_id: str) -> bool:
        """
        Removes a previously created task.

        :param job_id: an existing job identifier.
        :return: true/false result status.
        """

        job = self.queue.fetch_job(job_id)

        if job:
            self.logger.info(f'Removing job `{job.id}` as requested')

            try:
                job.cancel()

            except InvalidJobOperation:
                self.logger.debug(f'Already removed job `{job.id}`')

                return True

            return True

        return False
