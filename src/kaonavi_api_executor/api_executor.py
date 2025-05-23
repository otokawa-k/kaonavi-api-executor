from typing import Generic

from .auth.access_token import AccessToken
from .api.api_model import ApiModel
from .types.typevars import TRequest, TResponse


class ApiExecutor(Generic[TRequest, TResponse]):
    def __init__(
        self, access_token: AccessToken, api: ApiModel[TRequest, TResponse]
    ) -> None:
        self.access_token = access_token
        self.api = api

    async def execute(self, no_cache: bool = False) -> TResponse:
        if not self.api.url:
            raise ValueError("API URL is not set.")

        headers = {
            **self.api.headers,
            "Content-Type": "application/json",
            "Kaonavi-Token": await self.access_token.get(),
        }

        response = await self.api.http_method.send(
            url=self.api.url,
            params=self.api.params,
            headers=headers,
            auth=self.api.auth,
            data=self.api.data,
            no_cache=no_cache,
        )

        if response.status_code != 200:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )

        return self.api.parse_response(response.json())
