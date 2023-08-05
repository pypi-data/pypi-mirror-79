from typing import List, Callable, Any, Optional
import traceback
from abc import ABC, abstractmethod


import vk_api
import requests
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotLongPoll
from vk_api.vk_api import VkApiMethod, VkApi

# TODO Добавить логирование


class Bot:
    api: VkApiMethod
    longpoll: VkBotLongPoll
    commands: List['Command']
    args: List['Arg']

    command_factory: 'CommandFactory'
    arg_factory: 'ArgFactory'

    def __init__(self, token, group_id):
        self.commands = []
        self.args = []

        session = vk_api.VkApi(token=token)
        self.api = session.get_api()
        self.longpoll = VkBotLongPoll(session, group_id)

        self.command_factory = CommandFactory(self)
        self.arg_factory = ArgFactory(self)

    @staticmethod
    def find_key(text: str, keys: List[str], all_text: bool = False):
        for key in keys:
            if key in text if all_text else text.startswith(key):
                return True
        return False

    def execute_command(self, event: VkBotMessageEvent) -> str:
        result = None
        text = event.message['text'].lower()
        for command in self.commands:
            if self.find_key(text, command.keys, command.all_text):
                result = command(event)
        return result

    def command(self, keys: List[str], all_text: bool = False):
        def _(func):
            self.commands.append(
                self.command_factory.create(func, keys, all_text))
            return func
        return _

    def arg(self, name: Optional[str] = None):
        def _(func):
            self.args.append(self.arg_factory.create(func, name))
            return func
        return _

    def run(self):
        while True:
            try:
                for event in self.longpoll.listen():
                    self.execute_command(event)
            except KeyboardInterrupt:
                break
            except requests.exceptions.ReadTimeout:
                pass  # Вк не ответил
            except Exception:
                traceback.print_exc()


class Factory(ABC):
    __slots__ = ('bot', )
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    @abstractmethod
    def create(self, *args, **kwargs):
        pass


class CommandFactory(Factory):
    def create(self, func: Callable, keys: List[str], all_text):
        return Command(self.bot, func, keys, all_text)


class ArgFactory(Factory):
    def create(self, func: Callable, name: str):
        return Arg(self.bot, func, name)


class EventApi:

    def __init__(self, api, event):
        self.api = api
        self.event = event

    def reply(self, **kwargs):
        self.api.messages.send(
            peer_id=self.event.message["peer_id"], **kwargs, reply_to=self.event.message["id"], random_id=0)


class Command:
    __slots__ = ('bot', 'func', 'keys', 'all_text')

    bot: Bot
    func: Callable[..., str]
    keys: List[str]
    all_text: bool

    def __init__(self, bot: Bot, func: Callable, keys: List[str], all_text: bool):
        self.bot = bot
        self.func = func
        self.keys = keys

        self.all_text = all_text

    def __call__(self, event: VkBotMessageEvent) -> str:
        done_args = []
        for func_arg in self.func.__code__.co_varnames:
            for g_arg in self.bot.args:
                if g_arg.name == func_arg:
                    done_args.append(g_arg(event))
        return self.func(EventApi(self.bot.api, event), *done_args)


class Arg:
    __slots__ = ('name', 'func', 'bot')
    name: str
    func: Callable[[VkBotMessageEvent, VkApiMethod], Any]
    bot: Bot

    def __init__(self, bot: Bot, func: Callable, name: str):
        self.bot = bot
        self.name = name or func.__code__.co_name.lstrip('_')
        self.func = func

    def __call__(self, event: VkBotMessageEvent):
        return self.func(event, self.bot)
