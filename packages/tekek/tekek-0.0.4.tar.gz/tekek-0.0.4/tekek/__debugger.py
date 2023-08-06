import logging
import asyncio

from typing import List, Any, Optional

import requests

from .__message import __Message as Message
from .__level import __Level as Level


class __Debugger:
    def __init__(
            self,
            verbosity: int = 1,
            log_to_console: bool = True,
            log_to_file: bool = False,
            log_to_server: bool = False,
            logger: logging.Logger = logging.getLogger('Tekek-Logger')
    ):
        self.__verbosity: int = verbosity
        self.__log_to_console: bool = log_to_console
        self.__log_to_file: bool = log_to_file
        self.__log_to_server: bool = log_to_server

        if not logger:
            logger: logging.Logger = logging.getLogger('Tekek-Logger')
        self.__logger: logging.Logger = logger

        self.__queue: List[Message] = []

        logging.info("Tekek currenly very hungry and searching for spot")
        for i in range(5):
            if self.__start():
                logging.info("Perfect Spot for hunting reached by Tekek!")
                break
            logging.info("Tekek fell from it's spot! :(")

    async def __add_to_queue(self, message: Message) -> bool:
        """ Add to Queue

        :return bool:
        """
        try:
            self.__queue.append(message)
            return True
        except Exception as e:
            raise RuntimeError("Failed to add to queue {}".format(e))

    async def __pop_from_queue(self, index: int) -> Optional[Message]:
        """ Pop from Queue

        :return Message:
        """
        try:
            msg: Message = self.__queue.pop(index)
            return msg
        except Exception as e:
            raise RuntimeError("Failed to pop from queue {}".format(e))

    @staticmethod
    async def __to_console(message: Message):
        try:
            if message.level == Level.DEBUG:
                logging.debug(str(message))
            elif message.level == Level.INFO:
                logging.info(str(message))
            elif message.level == Level.SUCCESS:
                logging.info(str(message))
            elif message.level == Level.WARNING:
                logging.warning(str(message))
            elif message.level == Level.ERROR:
                logging.error(str(message))
            elif message.level == Level.CRITICAL:
                logging.critical(str(message))
        except:
            pass

    @staticmethod
    async def __to_file(message: Message):
        # TODO: Implement logging to file
        return

    @staticmethod
    async def __to_server(message: Message, tries: int = -1):
        # TODO: implement push logging to server
        requests
        return

    async def __log(self):
        # TODO: Implement smart logging, so the highest importance get pushed first
        msg: Message = self.__queue.pop(len(self.__queue)-1)
        asyncio.ensure_future(self.__to_console(msg))
        asyncio.ensure_future(self.__to_file(msg))
        asyncio.ensure_future(self.__to_server(msg))

    async def __timer(self):
        while True:
            if len(self.__queue) >= 1:
                asyncio.ensure_future(self.__log())

            await asyncio.sleep(1)

    async def __start(self) -> bool:
        try:
            asyncio.ensure_future(self.__timer())
        except:
            return False

        return True

    async def __make_message(self, identifier: str, content: Any, level: Level):
        """ Make message class, add to queue and do the logging algorithm

        :param identifier:
        :param content:
        :param level:
        :return str:
        """
        msg: Message = Message(identifier, content, level)
        await self.__add_to_queue(msg)

    # --- PUBLIC ---
    async def debug(self, identifier: str, content: Any):
        """ Log, an additional information, remainders, records

        :param identifier:
        :param content:
        :return:
        """
        asyncio.ensure_future(self.__make_message(identifier, content, Level.DEBUG))

    async def info(self, identifier: str, content: Any):
        """ Information, must know without any urgency

        :param identifier:
        :param content:
        :return:
        """
        asyncio.ensure_future(self.__make_message(identifier, content, Level.INFO))

    async def success(self, identifier: str, content: Any):
        """ Success Information, process has ben sucessfully ran

        :param identifier:
        :param content:
        :return:
        """
        asyncio.ensure_future(self.__make_message(identifier, content, Level.SUCCESS))

    async def warning(self, identifier: str, content: Any):
        """ Warning, process(es) encounter something that not suppose to happen, but still can be handled

        :param identifier:
        :param content:
        :return:
        """
        asyncio.ensure_future(self.__make_message(identifier, content, Level.WARNING))

    async def error(self, identifier: str, content: Any):
        """ Warning, process(es) errored out, still can be handled, but urgently need an attention

        :param identifier:
        :param content:
        :return:
        """
        asyncio.ensure_future(self.__make_message(identifier, content, Level.ERROR))

    async def critical(self, identifier: str, content: Any):
        """ Warning, process(es) errored out, program exit unexpectedly

        :param identifier:
        :param content:
        :return:
        """
        asyncio.ensure_future(self.__make_message(identifier, content, Level.CRITICAL))
