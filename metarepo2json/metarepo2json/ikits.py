#!/usr/bin/env python3

import abc


class KitsInterface(metaclass=abc.ABCMeta):
    # todo: add to hub
    """
    https://realpython.com/python-interface/#using-abstract-method-declaration
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "load_data_source")
            and callable(subclass.load_data_source)
            and hasattr(subclass, "get_kits_data")
            and callable(subclass.get_kits_data)
        )

    @abc.abstractmethod
    def load_data_source(self, path):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_kits_data(self):
        """Get meta-repo kits from the data set"""
        raise NotImplementedError
