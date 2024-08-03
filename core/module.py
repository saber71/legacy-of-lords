import abc

from pydantic import BaseModel


class Module(abc.ABC, BaseModel):
    name: str
    description: str

    @abc.abstractmethod
    def install(self):
        pass

    @abc.abstractmethod
    def uninstall(self):
        pass
