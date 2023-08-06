__version__ = "0.0.1"
__verified__= False

import asyncio
import traceback

import discord
import fastapi
import typing
import uvicorn
import os
import json

from pydantic import BaseModel

from . import errors

_VARS = {
    "client": None
}

def set_vars(**kwargs):
    """
    Sets the variables to be used by the HTTPClient and webserver. This should only be called by :class:Client.

    :param kwargs: the (key, value) pairs to update the dict with.
    :return: the variables object
    """
    _VARS.update(kwargs)
    return _VARS

def get_vars(*keys):
    """
    Returns a single/list of values for each variable.

    :param keys: the keys to request. usually "bot", "function" and "cooldown".
    :return:
    """
    ret = []
    for key in keys:
        ret.append(_VARS.get(key.lower()))
    if len(ret) == 1:
        ret = ret[0]
    elif not ret:
        return None
    return ret

app = fastapi.FastAPI()

class BumpRequest(BaseModel):
    type: str  # REQUEST
    guild: str
    channel: str
    user: str


class MappedBumpRequest:
    """The Mapped BumpRequest.

    This class contains integers instead of snowflakes, or resolved object if bot is passed.
    ---
    values:
    - guild: Union[discord.Guild, int]
    - channel: Union[discord.TextChannel, int]
    - member: Union[discord.Member, None]
    - user: Union[discord.User, int]"""
    __slots__ = ("type", "guild", "channel", "member", "user")

    def __init__(self, raw: BumpRequest, bot = None):
        self.type = "REQUEST"
        self.guild = int(raw.guild)
        self.channel = int(raw.channel)
        self.user = int(raw.user)
        if bot:
            self.guild = bot.get_guild(self.guild) or self.guild  # or for fallbacks.
            self.channel = bot.get_channel(self.channel) or self.channel
            self.user = bot.get_user or self.channel
        if isinstance(self.guild, discord.Guild):
            self.member = self.guild.get_member(int(raw.user))
        else:
            self.member = None
    
    async def send(self, *args, **kwargs):
        """Sends a message to source channel"""
        if not isinstance(self.channel, discord.TextChannel):
            raise TypeError("Expected value TextChannel for self.channel, got int")
        if not self.channel.permissions_for(self.guild.me).send_messages:
            raise commands.BotMissingPermissions("send_messages")
        return await self.channel.send(*args, **kwargs)


class Client:
    def __init__(self, bot, bump_function: typing.Union[callable, str], *, bump_cooldown: int = 3600):
        self.ready = False
        self.server = None
        self.config = None
        self.task = None
        self.func = bump_function
        self.bot = bot
        self.cooldown = bump_cooldown
        set_vars(client=self)

    def init_server(self, host: str = "127.0.0.1", port: int = 1234, *, reload_on_file_edit: bool = False):
        """Initializes the internal server for use"""
        if self.ready:
            raise errors.StateException(True, False, message="Server is already initialized")
        self.config = uvicorn.Config(
            app,
            host,
            port,
            use_colors=False,
            reload=reload_on_file_edit
        )
        self.server = uvicorn.Server(self.config)
        self.ready = True
        return True

    def __verify_config_file(self):
        pass

    def start_server(self):
        """Starts the internal server, allowing incoming requests."""
        if self.task:
            raise errors.StateException(
                True,
                False,
                message=f"Internal task is already running. Try `Client.stop_server()` first."
            )
        elif not self.ready:
            raise errors.StateException(
                False,
                True,
                message=f"Server is not initialized!"
            )
        self.task = asyncio.get_event_loop().create_task(self.server.serve())
        # self.task = asyncio.create_task(self.server.serve())
        return True

    def stop_server(self):
        """Stops the internal server, denying incoming requests."""
        if not self.task:
            raise errors.StateException(
                False,
                True,
                message=f"Internal task is not already running. Try `Client.start_server()` first."
            )
        try:
            self.task.cancel()
        except:
            pass
        finally:
            return True

    async def _parse_function(self):
        if isinstance(self.func, str):
            func = self.bot.get_command(self.func.lower())
            if not self.func:
                raise TypeError(f"Command '{self.func}' doesn't exist. Unable to retrieve callback.")
            return func.callback
        else:
            return self.func

    async def request(self, req: fastapi.Request, body: BumpRequest):
        """The internal function. DO NOT CALL THIS!"""
        body = MappedBumpRequest(body, self.bot)
        self.bot.dispatch("sblp_request_start", body)
        try:
            res = await discord.utils.maybe_coroutine(await self._parse_function(), body=body, bot=self.bot)
        except Exception as e:
            traceback.print_exc()
            return fastapi.responses.JSONResponse(
                {
                    "type": "ERROR",
                    "code": "OTHER",
                    "message": f"Internal Error: {e}"
                },
                500
            )
        else:
            if isinstance(res, int):
                bumped_to = res
            else:
                bumped_to = -1
            return fastapi.responses.JSONResponse(
                {
                    "type": "FINISHED",
                    "response": "0",
                    "amount": bumped_to,
                    "nextBump": self.cooldown
                },
                200
            )

@app.post("/sblp/request")
async def sblp_request(req: fastapi.Request, body: BumpRequest):
    client: Client = get_vars("client", "Filler")[0]
    if client is None:
        raise errors.StateException(False, True, message="Client doesn't even exist yet. How tf did you get here?")
    else:
        client: Client
        await client.request(req, body)
