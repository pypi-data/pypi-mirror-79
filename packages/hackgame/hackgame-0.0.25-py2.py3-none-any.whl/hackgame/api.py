from datetime import datetime
from json import JSONDecodeError
from typing import List, Type, TypeVar, Generic, Optional

import requests

from hackgame.models import (
    World,
    AccessToken,
    Player,
    Account,
    Network,
    Connection,
    Program,
    Ice,
    ActionResult,
    ActionError,
    ErrorCode,
)


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Token {self.token}"
        return r


SERVER_HOSTS = {
    "local": "http://localhost:8000",
    "dev": "https://hackgame.dev.rachsharp.co.uk",
    "prod": "https://hackgame.rachsharp.co.uk",
}
HACKGAME_SERVER = "https://hackgame.dev.rachsharp.co.uk"
# HACKGAME_SERVER = "http://localhost:8000"
API_BASE = "/api"

Resource = TypeVar("Resource")


def _get_action_error_message(response) -> Optional[str]:
    """
    get text error message to display, for some status codes response.text
    will just be ugly and useless
    """
    if response.status_code == 404:
        message = None
    elif response.status_code == 500:
        message = ":( something went wrong server-side"
    else:
        message = response.text
    return message


class ObjectEndpoint(Generic[Resource]):
    def __init__(self, endpoint: str, object_class: Type[Resource], client):
        self.endpoint = endpoint
        self._class = object_class
        self._client = client

    @property
    def url(self) -> str:
        return f"{self._client.host}{API_BASE}/{self.endpoint}/"

    def create(self, data) -> Resource:
        response = self._client.session.post(self.url, data=data)
        response.raise_for_status()
        response = self._client.session.get(
            f"{self.url}{response.json()['public_uuid']}/"
        )
        return self._class(**response.json())

    def get(self, public_uuid) -> Resource:
        response = self._client.session.get(f"{self.url}{public_uuid}/")
        response.raise_for_status()
        obj = self._class(**response.json())
        return obj

    def list(self) -> List[Resource]:
        response = self._client.session.get(self.url)
        response.raise_for_status()
        return [self._class(**item) for item in response.json()]

    def proxy(self, public_uuid) -> ActionResult:
        response = self._client.session.post(f"{self.url}{public_uuid}/proxy/")
        try:
            action_result = ActionResult(
                status_code=response.status_code, **response.json()
            )
        except (TypeError, JSONDecodeError):
            message = _get_action_error_message(response)
            action_result = ActionResult(
                success=False,
                status_code=response.status_code,
                errors=[ActionError(code=ErrorCode.generic, message=message)],
            )
        return action_result

    def post(self, public_uuid, data) -> ActionResult:
        response = self._client.session.post(
            f"{self.url}{public_uuid}/post/", json=data
        )

        # todo how to handle 500s but not 4XXs
        # todo also handle invalid player tokens
        try:
            action_result = ActionResult(
                status_code=response.status_code, **response.json()
            )
        except (TypeError, JSONDecodeError):
            message = _get_action_error_message(response)
            action_result = ActionResult(
                success=False,
                status_code=response.status_code,
                errors=[ActionError(code=ErrorCode.generic, message=message)],
            )
        return action_result

    def transfer(self, public_uuid, data) -> ActionResult:
        response = self._client.session.post(
            f"{self.url}{public_uuid}/transfer/", json=data,
        )
        try:
            action_result = ActionResult(
                status_code=response.status_code, **response.json()
            )
        except (TypeError, JSONDecodeError):
            message = _get_action_error_message(response)
            action_result = ActionResult(
                success=False,
                status_code=response.status_code,
                errors=[ActionError(code=ErrorCode.generic, message=message)],
            )
        return action_result

    def describe(self, public_uuid) -> ActionResult:
        response = self._client.session.post(f"{self.url}{public_uuid}/describe/")
        try:
            action_result = ActionResult(
                status_code=response.status_code, **response.json()
            )
        except (TypeError, JSONDecodeError):
            message = _get_action_error_message(response)
            action_result = ActionResult(
                success=False,
                status_code=response.status_code,
                errors=[ActionError(code=ErrorCode.generic, message=message)],
            )
        return action_result

    def messages(self, public_uuid) -> List[str]:
        return self._client.session.get(
            f"{self.url}{public_uuid}/messages/"
        ).json()


class HackgameClient(object):
    def __init__(
        self,
        player_token: str,
        host: str,
        token: Optional[str] = None,
        endpoint_cls=ObjectEndpoint,
        **endpoint_kwargs,
    ):
        """
        :param player_token:
            Actual Secure Authentication Token, to determine which real
            person is playing the game.
        :param token:
            Insecure Token to determine what Object this Hackgame
            Client will be acting as.
        """
        session = requests.Session()

        self.host = host

        self.game_token = token
        if self.game_token is not None:
            session.headers.update({"Access-Token": self.game_token})

        session.auth = BearerAuth(token=player_token)
        self.session = session

        self.players = endpoint_cls[Player](
            "players", Player, client=self, **endpoint_kwargs
        )
        self.accounts = endpoint_cls[Account](
            "accounts", Account, client=self, **endpoint_kwargs
        )
        self.tokens = endpoint_cls[AccessToken](
            "tokens", AccessToken, client=self, **endpoint_kwargs
        )
        self.worlds = endpoint_cls[World](
            "worlds", World, client=self, **endpoint_kwargs
        )
        self.networks = endpoint_cls[Network](
            "networks", Network, client=self, **endpoint_kwargs
        )
        self.connections = endpoint_cls[Connection](
            "connections", Connection, client=self, **endpoint_kwargs
        )
        self.programs = endpoint_cls[Program](
            "programs", Program, client=self, **endpoint_kwargs
        )

        self.ice = endpoint_cls[Ice]("ice", Ice, client=self, **endpoint_kwargs)

        self.registry = {
            Player: self.players,
            Account: self.accounts,
            AccessToken: self.tokens,
            World: self.worlds,
            Network: self.networks,
            Connection: self.connections,
            Program: self.programs,
            Ice: self.ice,
        }

    def __getitem__(self, item) -> ObjectEndpoint:
        return self.registry[item]

    def messages(self, after: datetime = None) -> List[str]:
        url = f"{self.tokens.url}{self.game_token}/messages/"
        params = {}
        if after is not None:
            params["after"] = after.isoformat()
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()["messages"]
