import typing
import functools
import asyncio

import yaml
import jinja2
from starlette.responses import (
    Response,
    HTMLResponse,
    PlainTextResponse,
    JSONResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse,
)
from starlette.background import BackgroundTask

from ..types import Scope, Receive, Send


__all__ = [
    "automatic",
    "Response",
    "HTMLResponse",
    "PlainTextResponse",
    "JSONResponse",
    "YAMLResponse",
    "RedirectResponse",
    "StreamingResponse",
    "FileResponse",
    "TemplateResponse",
]


class TemplateResponse(Response):
    media_type = "text/html"

    def __init__(
        self,
        name: str,
        context: dict,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ):
        if "request" not in context:
            raise ValueError('context must include "request".')
        self.env: jinja2.Environment = context["request"].scope["app"].jinja_env
        self.template = self.env.get_template(name)
        self.context = context
        super().__init__(None, status_code, headers, media_type, background)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self.env.enable_async:  # type: ignore
            content = await self.template.render_async(self.context)
        else:
            content = self.template.render(self.context)
        self.body = self.render(content)
        self.headers.setdefault("content-length", str(len(self.body)))

        extensions = self.context.get("request", {}).get("extensions", {})
        if "http.response.template" in extensions:
            await send(
                {
                    "type": "http.response.template",
                    "template": self.template,
                    "context": self.context,
                }
            )
        await super().__call__(scope, receive, send)


class YAMLResponse(Response):
    media_type = "text/yaml"

    def render(self, content: typing.Any) -> bytes:
        return yaml.dump(content, indent=2).encode("utf8")


class EventResponse(Response):
    r"""
    Server send event Response 🔗[MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)

    You have to deal with several fields specified in the SSE standard,
    but sending ping frames is automatic, and its time period is controlled by `ping_interval`.

    Ping frame like `event: ping\r\n\r\n`.

    generator example:

        async def generator_example():
            yield '''event: date\r\ndata: {"date": "2020-12-31"}'''

    """

    media_type = "text/event-stream"
    required_headers = {"Cache-Control": "no-cache", "Connection": "keep-alive"}

    def __init__(
        self,
        generator: typing.AsyncGenerator[str, None],
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
        *,
        ping_interval: int = 3,
    ) -> None:
        if headers:
            headers.update(self.required_headers)
        else:
            headers = dict(self.required_headers)

        super().__init__(None, status_code, headers, media_type, background)
        self.generator = generator
        self.ping_interval = ping_interval

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        done, pending = await asyncio.wait(
            (self.keep_alive(send), self.send_event(send)),
            return_when=asyncio.FIRST_COMPLETED,
        )
        [task.cancel() for task in pending]
        [task.result() for task in done]
        await send({"type": "http.response.body", "body": b""})

        if self.background is not None:
            await self.background()

    async def send_event(self, send: Send) -> None:
        async for chunk in self.generator:
            await send(
                {
                    "type": "http.response.body",
                    "body": f"{chunk.strip()}\r\n\r\n".encode(self.charset),
                    "more_body": True,
                }
            )

    async def keep_alive(self, send: Send) -> None:
        while True:
            await asyncio.sleep(self.ping_interval)
            await send(
                {
                    "type": "http.response.body",
                    "body": "event: ping\r\n\r\n".encode("utf8"),
                    "more_body": True,
                }
            )


def convert(response: typing.Any) -> Response:
    """
    shortcut for automatic

    Example:

        response = convert(response)

    It is equivalent to:

        if isinstance(response, tuple):
            response = automatic(*response)
        else:
            response = automatic(response)

    """
    if isinstance(response, tuple):
        return automatic(*response)
    else:
        return automatic(response)


@functools.singledispatch
def automatic(*args: typing.Any) -> Response:
    # Response or Response subclass
    if isinstance(args[0], Response):
        return args[0]

    raise TypeError(f"Cannot find automatic handler for this type: {type(args[0])}")


@automatic.register(type(None))
def _none(ret: typing.Type[None]) -> typing.NoReturn:
    raise TypeError(
        "Get 'None'. Maybe you need to add a return statement to the function."
    )


@automatic.register(tuple)
@automatic.register(list)
@automatic.register(dict)
def _json(
    body: typing.Tuple[tuple, list, dict], status: int = 200, headers: dict = None
) -> Response:
    return JSONResponse(body, status, headers)


@automatic.register(str)
@automatic.register(bytes)
def _plain_text(
    body: typing.Union[str, bytes], status: int = 200, headers: dict = None
) -> Response:
    return PlainTextResponse(body, status, headers)
