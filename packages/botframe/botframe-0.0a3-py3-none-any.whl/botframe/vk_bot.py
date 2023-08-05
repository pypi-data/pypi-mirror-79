from typing import List, Callable, Any, Optional

import vk_api
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotLongPoll
from vk_api.vk_api import VkApiMethod, VkApi

# TODO Добавить логирование


class ApiMethod(VkApiMethod):

    def __init__(self, vk: Any, method: Any = None):
        super().__init__(vk, method)

    def reply(self, event, **kwargs):
        self.messages.send(
            peer_id=event.message["peer_id"], **kwargs, reply_to=event.message["id"], random_id=0)


class Vk:
    session: VkApi
    api: ApiMethod
    longpoll: VkBotLongPoll

    def __init__(self, token, group_id):
        self.session = vk_api.VkApi(token=token)
        self.api = ApiMethod(self.session)
        self.longpoll = VkBotLongPoll(self.session, group_id)


class Bot:
    vk: Vk
    commands: List['Command']
    args: List['Arg']

    command_factory: 'CommandFactory'
    arg_factory: 'ArgFactory'

    def __init__(self, token, group_id):
        self.commands = []
        self.args = []
        self.vk = Vk(token, group_id)

        self.command_factory = CommandFactory(self.vk.api, self.args)
        self.arg_factory = ArgFactory(self.vk.api)

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
                for event in self.vk.longpoll.listen():
                    self.execute_command(event)
            except Exception as e:
                print(e)


class Factory:
    _api: VkApiMethod
    _args: Optional[List['Arg']]

    def __init__(self, api: VkApiMethod, args: Optional[List['Arg']] = None):
        self._api = api
        self._args = args


class CommandFactory(Factory):
    def create(self, func: Callable, keys: List[str], all_text):
        return Command(func, keys, self._api, self._args, all_text)


class ArgFactory(Factory):
    def create(self, func: Callable, name: str):
        return Arg(func, name, self._api)


class Command:

    _func: Callable[..., str]
    __args: List['Arg']
    keys: List[str]
    __api: VkApiMethod
    all_text: bool

    def __init__(self, func: Callable, keys: List[str], api, args: List['Arg'], all_text):
        self.__api = api
        self._func = func
        self.keys = keys
        self.__args = args

        self.all_text = all_text

    def __call__(self, event: VkBotMessageEvent) -> str:
        done_args = []
        for func_arg in self._func.__code__.co_varnames:
            for g_arg in self.__args:
                if g_arg.name == func_arg:
                    done_args.append(g_arg(event))
        return self._func(*done_args)


class Arg:

    name: str
    _func: Callable[[VkBotMessageEvent, VkApiMethod], Any]
    __api: VkApiMethod

    def __init__(self, func: Callable, name: str, api: VkApiMethod):
        self.__api = api
        self.name = name or func.__code__.co_name.lstrip('_')
        self._func = func

    def __call__(self, event: VkBotMessageEvent):
        return self._func(event, self.__api)
