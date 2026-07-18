import httpx


class SubtitleAPIError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


class SubtitleAPIClient:
    def __init__(self, base_url="http://127.0.0.1:8000", timeout=30):
        self.client = httpx.Client(base_url=base_url.rstrip("/"), timeout=timeout)

    def _request(self, method, path, **kwargs):
        try:
            response = self.client.request(method, path, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            data = exc.response.json() if "application/json" in exc.response.headers.get("content-type", "") else {}
            detail = data.get("detail", "API request failed")
            raise SubtitleAPIError("API_ERROR", str(detail)) from exc
        except httpx.HTTPError as exc:
            raise SubtitleAPIError("API_UNAVAILABLE", "Cannot connect to the translation API") from exc

    def health(self): return self._request("GET", "/health").json()
    def providers(self): return self._request("GET", "/providers").json()
    def discover(self): return self._request("GET", "/providers/discover").json()
    def job(self, job_id): return self._request("GET", f"/jobs/{job_id}").json()
    def cancel(self, job_id): return self._request("POST", f"/jobs/{job_id}/cancel").json()
    def resume(self, job_id): return self._request("POST", f"/jobs/{job_id}/resume").json()
    def download(self, job_id):
        response = self._request("GET", f"/jobs/{job_id}/download")
        return response.content, response.headers.get("content-disposition", ""), response.headers.get("content-type", "text/plain")

    def create_translation(self, file, config):
        files = {"file": (file.name, file.getvalue(), "application/octet-stream")}
        return self._request("POST", "/translate", files=files, data={"request": config}).json()
