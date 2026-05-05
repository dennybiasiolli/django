from datetime import date

from django.forms import CharField, DateInput, Form
from django.test import override_settings
from django.utils import translation

from .base import WidgetTest


class DateInputTest(WidgetTest):
    widget = DateInput()

    def test_render_none(self):
        self.check_html(
            self.widget, "date", None, html='<input type="text" name="date">'
        )

    def test_render_value(self):
        d = date(2007, 9, 17)
        self.assertEqual(str(d), "2007-09-17")

        self.check_html(
            self.widget,
            "date",
            d,
            html='<input type="text" name="date" value="2007-09-17">',
        )
        self.check_html(
            self.widget,
            "date",
            date(2007, 9, 17),
            html=('<input type="text" name="date" value="2007-09-17">'),
        )

    def test_string(self):
        """
        Should be able to initialize from a string value.
        """
        self.check_html(
            self.widget,
            "date",
            "2007-09-17",
            html=('<input type="text" name="date" value="2007-09-17">'),
        )

    def test_format(self):
        """
        Use 'format' to change the way a value is displayed.
        """
        d = date(2007, 9, 17)
        widget = DateInput(format="%d/%m/%Y", attrs={"type": "date"})
        self.check_html(
            widget, "date", d, html='<input type="date" name="date" value="17/09/2007">'
        )

    @translation.override("de-at")
    def test_l10n(self):
        self.check_html(
            self.widget,
            "date",
            date(2007, 9, 17),
            html='<input type="text" name="date" value="17.09.2007">',
        )

    def test_fieldset(self):
        class TestForm(Form):
            template_name = "forms_tests/use_fieldset.html"
            field = CharField(widget=self.widget)

        form = TestForm()
        self.assertIs(self.widget.use_fieldset, False)
        self.assertHTMLEqual(
            form.render(),
            '<div><label for="id_field">Field:</label>'
            '<input id="id_field" name="field" required type="text"></div>',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_render_none(self):
        widget = DateInput()
        self.check_html(widget, "date", None, html='<input type="date" name="date">')

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_render_value(self):
        widget = DateInput()
        self.check_html(
            widget,
            "date",
            date(2007, 9, 17),
            html='<input type="date" name="date" value="2007-09-17">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    @translation.override("de-at")
    def test_html5_ignores_l10n(self):
        """HTML5 date inputs always use ISO format regardless of locale."""
        widget = DateInput()
        self.check_html(
            widget,
            "date",
            date(2007, 9, 17),
            html='<input type="date" name="date" value="2007-09-17">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_explicit_type_override(self):
        """Explicit attrs={'type': 'text'} overrides the HTML5 setting."""
        widget = DateInput(attrs={"type": "text"})
        self.check_html(
            widget,
            "date",
            date(2007, 9, 17),
            html='<input type="text" name="date" value="2007-09-17">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_explicit_format_respected(self):
        """Explicit format is used even when HTML5 input type is active."""
        widget = DateInput(format="%d/%m/%Y")
        self.check_html(
            widget,
            "date",
            date(2007, 9, 17),
            html='<input type="date" name="date" value="17/09/2007">',
        )
