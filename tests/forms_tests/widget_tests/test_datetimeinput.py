from datetime import datetime

from django.forms import CharField, DateTimeInput, Form
from django.test import override_settings
from django.utils import translation

from .base import WidgetTest


class DateTimeInputTest(WidgetTest):
    widget = DateTimeInput()

    def test_render_none(self):
        self.check_html(self.widget, "date", None, '<input type="text" name="date">')

    def test_render_value(self):
        """
        The microseconds are trimmed on display, by default.
        """
        d = datetime(2007, 9, 17, 12, 51, 34, 482548)
        self.assertEqual(str(d), "2007-09-17 12:51:34.482548")
        self.check_html(
            self.widget,
            "date",
            d,
            html=('<input type="text" name="date" value="2007-09-17 12:51:34">'),
        )
        self.check_html(
            self.widget,
            "date",
            datetime(2007, 9, 17, 12, 51, 34),
            html=('<input type="text" name="date" value="2007-09-17 12:51:34">'),
        )
        self.check_html(
            self.widget,
            "date",
            datetime(2007, 9, 17, 12, 51),
            html=('<input type="text" name="date" value="2007-09-17 12:51:00">'),
        )

    def test_render_formatted(self):
        """
        Use 'format' to change the way a value is displayed.
        """
        widget = DateTimeInput(
            format="%d/%m/%Y %H:%M",
            attrs={"type": "datetime"},
        )
        d = datetime(2007, 9, 17, 12, 51, 34, 482548)
        self.check_html(
            widget,
            "date",
            d,
            html='<input type="datetime" name="date" value="17/09/2007 12:51">',
        )

    @translation.override("de-at")
    def test_l10n(self):
        d = datetime(2007, 9, 17, 12, 51, 34, 482548)
        self.check_html(
            self.widget,
            "date",
            d,
            html=('<input type="text" name="date" value="17.09.2007 12:51:34">'),
        )

    def test_fieldset(self):
        class TestForm(Form):
            template_name = "forms_tests/use_fieldset.html"
            field = CharField(widget=self.widget)

        form = TestForm()
        self.assertIs(self.widget.use_fieldset, False)
        self.assertHTMLEqual(
            '<div><label for="id_field">Field:</label>'
            '<input id="id_field" name="field" required type="text"></div>',
            form.render(),
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_render_none(self):
        widget = DateTimeInput()
        self.check_html(
            widget,
            "date",
            None,
            html='<input type="datetime-local" name="date" step="1">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_render_value(self):
        widget = DateTimeInput()
        d = datetime(2007, 9, 17, 12, 51, 34, 482548)
        self.check_html(
            widget,
            "date",
            d,
            html=(
                '<input type="datetime-local" name="date" '
                'step="1" value="2007-09-17T12:51:34">'
            ),
        )
        self.check_html(
            widget,
            "date",
            datetime(2007, 9, 17, 12, 51),
            html=(
                '<input type="datetime-local" name="date" '
                'step="1" value="2007-09-17T12:51:00">'
            ),
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    @translation.override("de-at")
    def test_html5_ignores_l10n(self):
        """HTML5 datetime-local inputs always use ISO format."""
        widget = DateTimeInput()
        self.check_html(
            widget,
            "date",
            datetime(2007, 9, 17, 12, 51, 34),
            html=(
                '<input type="datetime-local" name="date" '
                'step="1" value="2007-09-17T12:51:34">'
            ),
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_explicit_type_override(self):
        """Explicit attrs={'type': 'text'} overrides the HTML5 setting."""
        widget = DateTimeInput(attrs={"type": "text"})
        self.check_html(
            widget,
            "date",
            datetime(2007, 9, 17, 12, 51, 34),
            html='<input type="text" name="date" value="2007-09-17 12:51:34">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_explicit_format_respected(self):
        """Explicit format is used even when HTML5 input type is active."""
        widget = DateTimeInput(format="%d/%m/%Y %H:%M")
        self.check_html(
            widget,
            "date",
            datetime(2007, 9, 17, 12, 51, 34),
            html=(
                '<input type="datetime-local" name="date" '
                'step="1" value="17/09/2007 12:51">'
            ),
        )
