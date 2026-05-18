import httpx


class BookerClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self._client.get(path, **kwargs)

    def post(self, path: str, **kwargs) -> httpx.Response:
        return self._client.post(path, **kwargs)

    def put(self, path: str, **kwargs) -> httpx.Response:
        return self._client.put(path, **kwargs)

    def patch(self, path: str, **kwargs) -> httpx.Response:
        return self._client.patch(path, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self._client.delete(path, **kwargs)

    def set_cookie(self, name: str, value: str) -> None:
        self._client.cookies.set(name, value)
