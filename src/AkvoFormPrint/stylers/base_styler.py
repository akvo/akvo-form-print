from abc import ABC, abstractmethod
from AkvoFormPrint.models import FormModel


class BaseStyler(ABC):
    @abstractmethod
    def render_html(self, form_model: FormModel) -> str:
        pass

    @abstractmethod
    def render_pdf(self, form_model: FormModel) -> bytes:
        pass
