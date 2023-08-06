import re
from urllib.parse import urlparse


class GeminiUrl:
    PROTOCOL = "gemini"
    __slots__ = ("host", "port", "path", "query")
    host: str
    port: int
    path: str
    query: str

    def __init__(self, host, port, path, query):
        """
        You probably don't want to use this constructor directly.
        Use one of the parse methods instead.
        """
        self.host = host
        self.port = port
        self.path = path
        self.query = query

    def __repr__(self):
        return f"{self.PROTOCOL}://{self.host}:{self.port}{self.path}{('?' + self.query) if self.query else ''}"

    def without_protocol(self):
        return f"{self.host}{(':'+self.port) if self.port != 1965 else ''}{self.path}{('?' + self.query) if self.query else ''}"

    @classmethod
    def parse(cls, text, current_url):
        assert not re.search(r"\s", text), "Url should not contain any whitespace!"

        protocol = urlparse(text).scheme
        if protocol == cls.PROTOCOL:
            return cls.parse_absolute_url(text)

        if protocol:
            raise UnsupportedProtocolError(protocol)

        # absolute url with scheme omitted
        # for example, "//example.com/foo"
        if text.startswith("//"):
            return cls.parse_absolute_url("gemini:" + text)

        if current_url is None:
            raise NonAbsoluteUrlWithoutContextError(text)

        # relative url starting from top level
        if text.startswith("/"):
            path, query = tuple((text + "?").split("?")[:2])
            return GeminiUrl(current_url.host, current_url.port, path, query)

        # just query:
        if text.startswith("?"):
            query = text[1:]
            return GeminiUrl(
                current_url.host, current_url.port, current_url.path, query
            )

        # just relative url:
        # trim stuff after the last `/` - for example:
        #   current url: gemini://example.com/foo/bar
        #   raw url text: yikes
        #   => parsed url: gemini://example.com/foo/yikes
        current_path = current_url.path[: current_url.path.rfind("/") + 1]
        if current_path == "":
            current_path = "/"

        path, query = tuple((text + "?").split("?")[:2])
        current_path += path
        return GeminiUrl(current_url.host, current_url.port, current_path, query)

    @staticmethod
    def parse_absolute_url(text):
        # TODO: urlparse doesn't seem that foolproof. Revisit later.
        parsed = urlparse(text)
        return GeminiUrl(
            parsed.hostname, parsed.port or 1965, parsed.path, parsed.query
        )

