import pytest
from AkvoFormPrint.stylers.base_styler import BaseStyler
from AkvoFormPrint.models import FormModel


class MockStyler(BaseStyler):
    def render_html(self, form_model: FormModel) -> str:
        raise NotImplementedError()

    def render_pdf(self, form_model: FormModel) -> bytes:
        raise NotImplementedError()


def test_base_styler_render_html():
    styler = MockStyler()
    form = FormModel(title="Test Form", sections=[])
    with pytest.raises(NotImplementedError):
        styler.render_html(form)


def test_base_styler_render_pdf():
    styler = MockStyler()
    form = FormModel(title="Test Form", sections=[])
    with pytest.raises(NotImplementedError):
        styler.render_pdf(form)


def test_base_styler_set_form_model():
    styler = MockStyler()
    form = FormModel(title="Test Form", sections=[])
    styler.form_model = form
    assert styler.form_model == form
    assert styler.form_model.title == "Test Form"
