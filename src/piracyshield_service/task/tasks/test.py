from piracyshield_service.task.base import BaseTask

class TestTask(BaseTask):

    def run(self, *args: any, **kwargs: any) -> bool:
        print('Hello world')

    def before_run(self):
        pass

    def after_run(self):
        pass

    def on_failure(self):
        pass

def test_task_caller():
    t = TestTask()

    return t.execute()
