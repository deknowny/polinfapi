import abc
import dataclasses
import io
import typing

from polinfapi.client import BaseSyncClient, RequestsClient
from polinfapi.parser import RawTask, parse_to_raw_tasks
from polinfapi.utils import download_image

TaskType = typing.TypeVar("TaskType")


@dataclasses.dataclass
class BaseTask(abc.ABC):
    raw: RawTask
    task_url: typing.ClassVar[str]

    @classmethod
    @abc.abstractmethod
    def _init_by_raw_task(cls: TaskType, raw_task: RawTask) -> TaskType:
        pass

    @classmethod
    def fetch(
        cls: typing.Type[TaskType],
        client: typing.Optional[BaseSyncClient] = None,
    ) -> typing.List[TaskType]:
        with RequestsClient.exists_or_new(client) as session:
            tasks_content = session.get(cls.task_url)
            tasks = [
                cls._init_by_raw_task(raw_task)
                for raw_task in parse_to_raw_tasks(tasks_content)
            ]
            return tasks


@dataclasses.dataclass
class ContainsImageMixin:
    gif_url: str

    def download_image(self) -> io.BytesIO:
        return download_image(self.gif_url)
