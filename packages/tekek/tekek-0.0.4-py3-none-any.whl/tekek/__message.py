import time

from datetime import datetime
from typing import Any, List

from .__level import __Level as Level


class __Message:
    identifier: str = None
    content: str = None
    level: Level = Level.INFO

    def __init__(self, timestamp: time.struct_time, identifier: str, content: Any, level: Level):
        self.timestamp = timestamp
        self.identifier: str = identifier
        self.content: str = self.__convert_to_str(content)
        self.level: Level = level

    @staticmethod
    def __convert_to_str(content: Any) -> str:
        c = None
        try:
            c = str(content)
        except:
            try:
                c = repr(content)
            except:
                ...

        return c

    def __convert_to_content(self) -> str:
        return "[{}][{}][{}] {}".format(
            time.strftime("%d-%m %H:%M:%S", self.timestamp),
            self.identifier,
            self.level.value,
            self.content
        )

    def __repr__(self):
        return self.__convert_to_content()

    def __str__(self):
        return self.__convert_to_content()
