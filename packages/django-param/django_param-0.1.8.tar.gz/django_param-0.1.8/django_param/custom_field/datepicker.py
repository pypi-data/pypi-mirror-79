from django.forms import DateTimeInput
from django_param.custom_widget.datepicker_widget import DatePickerWidget


class DateTimePicker(DateTimeInput):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = DatePickerWidget
        super().__init__(*args, **kwargs)
