import hashlib
import hmac
import time
import urllib.parse

import requests


class MexcClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")

    def check_connection(self) -> tuple[bool, str]:
        try:
            timestamp = int(time.time() * 1000)
            params = {"timestamp": timestamp}
            query_string = urllib.parse.urlencode(params)
            signature = hmac.new(
                self.api_secret.encode("utf-8"),
                query_string.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            signed_query = f"{query_string}&signature={signature}"

            url = f"{self.base_url}/api/v3/account?{signed_query}"
            headers = {"X-MEXC-APIKEY": self.api_key}

            response = requests.get(url, headers=headers, timeout=10)
            if response.ok:
                return True, "OK"

            try:
                error_data = response.json()
                error_message = error_data.get("msg") or str(error_data)
            except ValueError:
                error_message = response.text or f"HTTP {response.status_code}"

            return False, error_message
        except requests.RequestException as exc:
            return False, str(exc)
        except Exception as exc:
            return False, str(exc)
