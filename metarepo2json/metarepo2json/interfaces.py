#!/usr/bin/env python3

import abc


def __init__(hub):
    global HUB
    HUB = hub


class KitsInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.hub = HUB

    # https://realpython.com/python-interface/#using-abstract-method-declaration

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "load_data")
            and callable(subclass.load_data)
            and hasattr(subclass, "process_data")
            and callable(subclass.process_data)
            and hasattr(subclass, "get_result")
            and callable(subclass.get_result)
        )

    @abc.abstractmethod
    async def load_data(self, path: str, **kwargs) -> None:
        """Load from the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    async def process_data(self):
        """Process loaded data"""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_result(self) -> list:
        """Get meta-repo kits from the data set"""
        raise NotImplementedError


class CategoriesInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.hub = HUB

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "load_data")
            and callable(subclass.load_data)
            and hasattr(subclass, "process_data")
            and callable(subclass.process_data)
            and hasattr(subclass, "get_result")
            and callable(subclass.get_result)
        )

    @abc.abstractmethod
    async def load_data(self, path: str, **kwargs) -> None:
        """Load from the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    async def process_data(self):
        """Process loaded data"""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_result(self) -> list:
        """Get meta-repo kits from the data set"""
        raise NotImplementedError


class CatPkgsInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.hub = HUB

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "load_data")
            and callable(subclass.load_data)
            and hasattr(subclass, "process_data")
            and callable(subclass.process_data)
            and hasattr(subclass, "get_result")
            and callable(subclass.get_result)
        )

    @abc.abstractmethod
    async def load_data(self, path: str, category: str, **kwargs) -> None:
        """Load from the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    async def process_data(self):
        """Process loaded data"""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_result(self) -> list:
        """Get meta-repo kits from the data set"""
        raise NotImplementedError
