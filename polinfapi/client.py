from __future__ import annotations

import abc
import contextlib
import dataclasses
import io
import typing

import requests


@dataclasses.dataclass
class BaseSyncClient(abc.ABC):
    @abc.abstractmethod
    def get(self, url: str) -> str:
        pass

    @abc.abstractmethod
    def download_raw(self, url: str) -> io.BytesIO:
        pass


@dataclasses.dataclass
class RequestsClient(BaseSyncClient):

    session: requests.Session

    @classmethod
    @contextlib.contextmanager
    def new(cls) -> typing.ContextManager[RequestsClient]:
        session = requests.Session()
        yield cls(session=session)
        session.close()

    @classmethod
    @contextlib.contextmanager
    def exists_or_new(
        cls, session: typing.Optional[BaseSyncClient] = None
    ) -> BaseSyncClient:
        if session is None:
            client_ctx = RequestsClient.new()
        else:
            client_ctx = contextlib.nullcontext(session)
        with client_ctx as client_conn:
            yield client_conn

    def download_raw(self, url: str) -> io.BytesIO:
        raw_image = self.session.get(url).content
        return io.BytesIO(raw_image)

    def get(self, url: str) -> str:
        page = self.session.get(url)
        return page.text
