from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TProvidedService = TypeVar("TProvidedService", bound=object)


class ServiceProvider(ABC, Generic[TProvidedService]):
    @abstractmethod
    def provide(self) -> TProvidedService:
        pass
