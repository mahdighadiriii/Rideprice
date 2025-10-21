from typing import Any, Dict, Optional

import httpx


class BaseHTTPClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        headers = {}
        if self.api_key:
            headers["Api-Key"] = self.api_key

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
