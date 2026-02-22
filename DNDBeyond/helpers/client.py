class DndBeyondClient:
    """Shared HTTP client for D&D Beyond homebrew endpoints."""

    def __init__(
        self,
        session,
        security_token: str,
        authenticity_token: str,
        verification_token: str = None,
        base_url: str = "https://www.dndbeyond.com",
    ):
        self.session = session
        self.security_token = security_token
        self.authenticity_token = authenticity_token
        self.verification_token = verification_token
        self.base_url = base_url
        self.last_error = None
        self.last_response = None

    def _build_url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    def get(self, path: str, params=None, timeout: int = 30):
        url = self._build_url(path)
        response = self.session.get(url, params=params, timeout=timeout)
        self.last_response = response
        return response

    def post(
        self,
        path: str,
        data=None,
        files=None,
        allow_redirects: bool = False,
        timeout: int = 30,
    ):
        url = self._build_url(path)
        response = self.session.post(
            url, data=data, files=files, allow_redirects=allow_redirects, timeout=timeout
        )
        self.last_response = response
        return response

    def record_response_error(self, response, url: str):
        error_details = {
            "status_code": response.status_code,
            "reason": response.reason,
            "url": url,
            "headers": dict(response.headers),
        }
        try:
            if response.headers.get("content-type", "").startswith("application/json"):
                error_details["response_body"] = response.json()
            else:
                error_details["response_preview"] = response.text[:500]
        except Exception:
            pass
        self.last_error = error_details

    def record_exception(self, exc: Exception):
        import traceback

        self.last_error = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback": traceback.format_exc(),
        }
