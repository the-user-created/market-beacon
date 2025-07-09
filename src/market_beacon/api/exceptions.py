from typing import Any

from requests import Response


class BitgetAPIError(Exception):
    """Base exception for all Bitget API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(status_code={self.status_code}): {self.message}"


class BitgetAPIRequestError(BitgetAPIError):
    """Raised for non-200 HTTP status codes or API-level errors (e.g., bad request)."""

    def __init__(self, response: Response):
        self.response = response
        try:
            body = response.json()
            msg = body.get("msg", "No error message provided")
        except Exception:
            body = None
            msg = response.text or "Failed to decode response"
        super().__init__(message=msg, status_code=response.status_code, response_body=body)
