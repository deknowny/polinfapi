import abc
import dataclasses
import io
import typing

from polinfapi.client import BaseSyncClient, RequestsClient
from polinfapi.parser import RawTask, parse_to_raw_tasks
from polinfapi.utils import download_image

TaskType = typing.TypeVar("TaskType")


class RawCode(typing.NamedTuple):
    lang: str
    code: str


@dataclasses.dataclass
class TaskModel:
    raw_task: RawTask
    question: str
    answer: str
    gif_url: typing.Optional[str] = None
    raw_codes: typing.List[RawCode] = dataclasses.dataclass(default_factory=list)
    input_data: typing.Optional[str] = None
    output_data: typing.Optional[str] = None

    @classmethod
    def fetch(cls, no: int, client: typing.Optional[BaseSyncClient] = None) -> typing.List[TaskModel]:
        with RequestsClient.exists_or_new(client) as session:
            tasks_content = session.get(cls.task_url)
            return [
                task_initors[no](raw_task)
                for raw_task in parse_to_raw_tasks(tasks_content)
            ]


    def download_gif(self) -> io.BytesIO:
        pass

    def gif_as_png(self) -> io.BytesIO:
        pass



def init_1_task(raw_task: RawTask) -> TaskModel:
    gif_name = task1_image_regex.search(raw_task.raw_text).group(
        "gif_name"
    )
    gif_url = POLYAKOV_BASE_GIF_URL + gif_name
    task_readable_text_parts = task1_image_regex.split(
        raw_task.raw_text, maxsplit=1
    )
    del task_readable_text_parts[1]
    task_readable_text = "".join(task_readable_text_parts)
    return TaskModel(
        answer=raw_task.raw_answer,
        question=task_readable_text,
        gif_url=gif_url,
        raw=raw_task,
    )


task_initors = {
    1: init_1_task
}


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
