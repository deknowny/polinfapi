import dataclasses
import re
import typing

from polinfapi.models.base import BaseTask, ContainsImageMixin, TaskType
from polinfapi.parser import RawTask
from polinfapi.utils import POLYAKOV_BASE_GIF_URL, POLYAKOV_BASE_URL

task1_image_regex = re.compile(r'<br/><img src="(?P<gif_name>\d+\.gif)"/?>')


@dataclasses.dataclass
class Task1ModelsAnalysis(BaseTask, ContainsImageMixin):
    question: str
    answer: str

    task_url: typing.ClassVar[str] = (
        POLYAKOV_BASE_URL
        + "/school/ege/gen.php?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on"
    )

    @classmethod
    def _init_by_raw_task(cls: TaskType, raw_task: RawTask) -> TaskType:
        gif_name = task1_image_regex.search(raw_task.raw_text).group(
            "gif_name"
        )
        gif_url = POLYAKOV_BASE_GIF_URL + gif_name
        task_readable_text_parts = task1_image_regex.split(
            raw_task.raw_text, maxsplit=1
        )
        del task_readable_text_parts[1]
        task_readable_text = "".join(task_readable_text_parts)
        return cls(
            answer=raw_task.raw_answer,
            question=task_readable_text,
            gif_url=gif_url,
            raw=raw_task,
        )

    @classmethod
    def _get_image_url(cls, raw_task: RawTask) -> str:
        gif_name = task1_image_regex.search(raw_task.raw_text).group(
            "gif_name"
        )
        return POLYAKOV_BASE_GIF_URL + gif_name



