# -*- coding: utf-8 -*-

from django import forms
from pandas import DataFrame
from django_param.custom_widget.dataframewidget import DataFrameWidget
from django.core.exceptions import ValidationError


class DataFrameField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = DataFrameWidget
        super().__init__(*args, **kwargs)

    def validate(self, value):
        # No need to validate dataframe
        if not isinstance(value, DataFrame):
            if value in self.empty_values and self.required:
                raise ValidationError(self.error_messages['required'], code='required')

    def run_validators(self, value):
        # No need to validate dataframe
        if not isinstance(value, DataFrame):
            if value in self.empty_values:
                return
            errors = []
            for v in self.validators:
                try:
                    v(value)
                except ValidationError as e:
                    if hasattr(e, 'code') and e.code in self.error_messages:
                        e.message = self.error_messages[e.code]
                    errors.extend(e.error_list)
            if errors:
                raise ValidationError(errors)
