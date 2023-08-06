from django import forms
from datetime import datetime, date


class DatePickerWidget(forms.Widget):
    template_name = 'django_param/datepicker/datepicker.html'

    class Media:
        css = {'all': ('django_param/datepicker/jquery.datetimepicker.min.css',)}
        js = [
            'django_param/datepicker/jquery.datetimepicker.full.js',
        ]

    def get_context(self, name, value, attrs):
        context = dict()
        context['widget'] = {
            'name': name,
            'is_hidden': self.is_hidden,
            'required': self.is_required,
            'value': self.format_value(value),
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name,
        }
        return context

    def value_from_datadict(self, data, files, name):
        """
        convert values into datetimeobject again.
        """
        date_time_str = data[name]
        if ":" in date_time_str:
            date_time_format = '%m-%d-%Y %H:%M'
            date_time_obj = datetime.strptime(date_time_str, date_time_format)
        else:
            date_time_format = '%m-%d-%Y'
            date_time_obj = datetime.strptime(date_time_str, date_time_format).date()
        return date_time_obj

    def format_value(self, value):
        # Convert to datetime to right string to display on the html.
        if isinstance(value, datetime):
            date_time_format = '%m-%d-%Y %H:%M'
            value = value.strftime(date_time_format)
        elif isinstance(value, date):
            date_time_format = '%m-%d-%Y'
            value = value.strftime(date_time_format)
        return value
