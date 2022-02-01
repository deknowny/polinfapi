import io
import typing

import PIL.Image

from polinfapi.client import BaseSyncClient, RequestsClient

POLYAKOV_BASE_URL = "https://kpolyakov.spb.ru"
POLYAKOV_BASE_GIF_URL = POLYAKOV_BASE_URL + "/cms/images/"


def download_image(
    url: str, client: typing.Optional[BaseSyncClient] = None
) -> io.BytesIO:
    with RequestsClient.exists_or_new(client) as session:
        gif = session.download_raw(url)
        processed_image = PIL.Image.open(gif)
        processed_image.seek(0)
        image = io.BytesIO()
        processed_image.save(image, format="PNG")
        return image
