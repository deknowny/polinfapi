import re
import typing

import bs4

task_no_regex = re.compile(
    r"document.write\( '\(№&nbsp;(?P<task_no>\d+)\) ' \);"
)
task_raw_text_regex = task_raw_answer_regex = re.compile(
    r"document.write\( changeImageFilePath\('(?P<raw_text>.+)'\) \);"
)


class RawTask(typing.NamedTuple):
    no: int
    raw_text: str
    raw_answer: str


def parse_to_raw_tasks(content: str) -> typing.List[RawTask]:
    soup = bs4.BeautifulSoup(content, "html.parser")
    tasks = soup.find_all("table", class_="vartopic")[0]
    tasks = typing.cast(bs4.Tag, tasks)
    tasks_blocks = tasks.find_all("tr")
    tasks_content = [task.find_all("script")[0].text for task in tasks_blocks]
    tasks_gen = iter(tasks_content)

    raw_tasks = []
    for task_data in tasks_gen:
        no = task_no_regex.search(task_data).group("task_no")
        raw_text = task_raw_text_regex.search(task_data).group("raw_text")
        answer_data = next(tasks_gen)
        raw_answer = task_raw_answer_regex.search(answer_data).group(
            "raw_text"
        )
        raw_task = RawTask(
            no=int(no), raw_text=raw_text, raw_answer=raw_answer
        )
        raw_tasks.append(raw_task)

    return raw_tasks
