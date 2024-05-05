import threading
from typing import TypeVar, Generic

# Класс для работы с переменными, к которым могут обращаться из различных потоков
# Переменные защищены мьютексами

T = TypeVar('T')


class AsyncFlag(Generic[T]):
    def __init__(self, value: T):
        self.__value = T
        self.__lock = threading.Lock()

    @property
    def value(self) -> T:
        with self.__lock:
            return self.__value

    @value.setter
    def value(self, value: T) -> None:
        with self.__lock:
            self.__value = value
