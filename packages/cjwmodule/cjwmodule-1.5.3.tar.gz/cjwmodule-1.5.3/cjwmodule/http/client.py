import contextlib
import ssl
from typing import BinaryIO, List, NamedTuple, Optional, Tuple

import httpx
from httpx import codes as http_status

from .errors import HttpError


class DownloadResult(NamedTuple):
    status_code: int
    reason_phrase: str
    headers: List[Tuple[bytes, bytes]]


async def download(
    url: str,
    wfile: BinaryIO,
    *,
    httpx_client: Optional[httpx.AsyncClient] = None,
    headers: List[Tuple[str, str]] = [],
    ssl: Optional[ssl.SSLContext] = None,
    total_timeout: int = 300,
    connect_timeout: int = 30
) -> DownloadResult:
    """
    Download from `url` and write (decoded) content bytes to `wfile`.

    Raise:

    * HttpError.InvalidUrl if `url` is not valid.
    * HttpError.Timeout if `total_timeout` or `connect_timeout` is exceeded.
    * HttpError.TooManyRedirects if there are too many redirects.
    * HttpError.NotSuccess if the status code isn't 200, 204 or 206.
    * HttpError.Generic (with a __cause__) if something else went wrong.
    """
    timeout = httpx.Timeout(total_timeout, connect=connect_timeout)

    async with contextlib.AsyncExitStack() as exit_stack:
        if httpx_client is None:
            httpx_client = await exit_stack.enter_async_context(
                httpx.AsyncClient(verify=ssl)
            )

        try:
            async with httpx_client.stream(
                "GET", url, timeout=timeout, headers=headers
            ) as response:
                async for blob in response.aiter_bytes():
                    wfile.write(blob)
                if response.status_code not in {
                    http_status.OK.value,
                    http_status.NO_CONTENT.value,
                    http_status.PARTIAL_CONTENT.value,
                }:
                    raise HttpError.NotSuccess(response)
                return DownloadResult(
                    response.status_code,
                    response.reason_phrase,
                    response.headers.raw,
                )
        except httpx.TimeoutException:
            raise HttpError.Timeout from None
        except (httpx.InvalidURL, httpx.UnsupportedProtocol):
            raise HttpError.InvalidUrl from None
        except httpx.TooManyRedirects:
            raise HttpError.TooManyRedirects from None
        except httpx.HTTPError as err:
            raise HttpError.Generic from err
