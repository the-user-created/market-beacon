import base64
import hmac
import time
from hashlib import sha256


def get_timestamp_ms() -> str:
    """Returns the current time as a string of milliseconds since Epoch."""
    return str(int(time.time() * 1000))


def generate_signature(
    timestamp: str, method: str, request_path: str, body: str, secret_key: str
) -> str:
    """
    Generates the HMAC-SHA256 signature for a Bitget API request.

    The string to sign is a concatenation of:
    timestamp + HTTP_METHOD + request_path + body
    """
    message = timestamp + method.upper() + request_path + body
    mac = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), digestmod=sha256)
    return base64.b64encode(mac.digest()).decode()
