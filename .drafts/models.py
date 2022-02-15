import dataclasses


class RawCode(typing.NamedTuple):
    lang: str
    code: str


@dataclasses.dataclass
class TaskModel:
    raw_task: RawTask
    question: str
    answer: str
    gif_url: str
    raw_codes: typing.List[RawCode]
    input_data: str
    output_data: str
    
