from piracyshield_component.config import Config

from redis import Redis
from rq import Queue

class TaskInstanceService:

    """
    Task instance class.
    """

    queue = None

    task_config = None

    database_redis_config = None
    task_connection_config = None

    def __init__(self):
        self._prepare_configs()

        self._prepare_connections()

    def _prepare_connections(self) -> None:
        self.redis_connection = Redis(
            host = self.database_redis_config.get('host'),
            port = self.database_redis_config.get('port'),
            db = self.task_config.get('database')
        )

        self.queue = Queue(
            self.task_config.get('queue_name'),
            connection = self.redis_connection
        )

    def _prepare_configs(self) -> None:
        self.task_config = Config('application').get('task')

        self.database_redis_config = Config('database/redis').get('connection')
