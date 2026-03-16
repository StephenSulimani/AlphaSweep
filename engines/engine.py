from abc import ABC, abstractmethod

from models.job import Job


class Engine(ABC):
    @abstractmethod
    def search(self) -> list[Job]:
        pass
