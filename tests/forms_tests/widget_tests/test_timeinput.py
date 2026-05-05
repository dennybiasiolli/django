from datetime import time

from django.forms import CharField, Form, TimeInput
from django.test import override_settings
from django.utils import translation

from .base import WidgetTest


class TimeInputTest(WidgetTest):
    widget = TimeInput()

    def test_render_none(self):
        self.check_html(
            self.widget, "time", None, html='<input type="text" name="time">'
        )

    def test_render_value(self):
        """
        The microseconds are trimmed on display, by default.
        """
        t = time(12, 51, 34, 482548)
        self.assertEqual(str(t), "12:51:34.482548")
        self.check_html(
            self.widget,
            "time",
            t,
            html='<input type="text" name="time" value="12:51:34">',
        )
        self.check_html(
            self.widget,
            "time",
            time(12, 51, 34),
            html=('<input type="text" name="time" value="12:51:34">'),
        )
        self.check_html(
            self.widget,
            "time",
            time(12, 51),
            html=('<input type="text" name="time" value="12:51:00">'),
        )

    def test_string(self):
        """Initializing from a string value."""
        self.check_html(
            self.widget,
            "time",
            "13:12:11",
            html=('<input type="text" name="time" value="13:12:11">'),
        )

    def test_format(self):
        """
        Use 'format' to change the way a value is displayed.
        """
        t = time(12, 51, 34, 482548)
        widget = TimeInput(format="%H:%M", attrs={"type": "time"})
        self.check_html(
            widget, "time", t, html='<input type="time" name="time" value="12:51">'
        )

    @translation.override("de-at")
    def test_l10n(self):
        t = time(12, 51, 34, 482548)
        self.check_html(
            self.widget,
            "time",
            t,
            html='<input type="text" name="time" value="12:51:34">',
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
        widget = TimeInput()
        self.check_html(
            widget,
            "time",
            None,
            html='<input type="time" name="time" step="1">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_render_value(self):
        widget = TimeInput()
        self.check_html(
            widget,
            "time",
            time(12, 51, 34, 482548),
            html='<input type="time" name="time" step="1" value="12:51:34">',
        )
        self.check_html(
            widget,
            "time",
            time(12, 51),
            html='<input type="time" name="time" step="1" value="12:51:00">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    @translation.override("de-at")
    def test_html5_ignores_l10n(self):
        """HTML5 time inputs always use ISO format regardless of locale."""
        widget = TimeInput()
        self.check_html(
            widget,
            "time",
            time(12, 51, 34),
            html='<input type="time" name="time" step="1" value="12:51:34">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_explicit_type_override(self):
        """Explicit attrs={'type': 'text'} overrides the HTML5 setting."""
        widget = TimeInput(attrs={"type": "text"})
        self.check_html(
            widget,
            "time",
            time(12, 51, 34),
            html='<input type="text" name="time" value="12:51:34">',
        )

    @override_settings(USE_HTML5_DATE_INPUT=True)
    def test_html5_explicit_format_respected(self):
        """Explicit format is used even when HTML5 input type is active."""
        widget = TimeInput(format="%H:%M")
        self.check_html(
            widget,
            "time",
            time(12, 51, 34),
            html='<input type="time" name="time" step="1" value="12:51">',
        )
