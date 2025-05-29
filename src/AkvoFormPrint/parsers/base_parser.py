from abc import ABC, abstractmethod
from AkvoFormPrint.models import FormModel


class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_input) -> FormModel:
        pass
