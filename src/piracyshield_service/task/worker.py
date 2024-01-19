from piracyshield_service.task.instance import TaskInstanceService

from rq import Worker

import threading

class TaskWorkerService(TaskInstanceService):

    """
    Task worker management.
    """

    worker = None

    def __init__(self):
        super().__init__()

        self._prepare_modules()

    def start(self) -> None:
        # spawn a thread to use a worker with scheduler
        worker_thread = threading.Thread(target = self.worker.work(
            with_scheduler = True
        ))

        worker_thread.start()

        worker_thread.join()

    def _prepare_modules(self) -> None:
        self.worker = Worker(
            [self.queue],
            connection = self.redis_connection
        )
