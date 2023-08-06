# -*- coding: utf-8 -*-
import pickle

from django import forms
from django_param.custom_widget.tuplefiled_widget import TupleFieldWidget, NumericTupleFieldWidget, XYTupleFieldWidget,\
    RangeTupleFieldWidget


class TupleField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = TupleFieldWidget
        fields = []
        raw_fields = kwargs.pop('fields', None)
        for key, value in raw_fields.items():
            for i in range(len(value)):
                fields.append(forms.CharField(initial=value[i]))
        super().__init__(fields, require_all_fields=False, *args, **kwargs)

    def compress(self, data_list):
        return pickle.dumps(self.initial)


class NumericTupleField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = NumericTupleFieldWidget
        fields = []
        raw_fields = kwargs.pop('fields', None)
        for key, value in raw_fields.items():
            for i in range(len(value)):
                fields.append(forms.CharField())
        super().__init__(fields, require_all_fields=False, *args, **kwargs)

    def compress(self, data_list):
        return pickle.dumps(self.initial)


class XYTupleField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = XYTupleFieldWidget
        fields = []
        raw_fields = kwargs.pop('fields', None)
        for key, value in raw_fields.items():
            for i in range(len(value)):
                fields.append(forms.CharField())
        super().__init__(fields, require_all_fields=False, *args, **kwargs)

    def compress(self, data_list):
        return pickle.dumps(self.initial)


class RangeTupleField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = RangeTupleFieldWidget
        fields = []
        raw_fields = kwargs.pop('fields', None)
        for key, value in raw_fields.items():
            for i in range(len(value)):
                fields.append(forms.CharField())
        super().__init__(fields, require_all_fields=False, *args, **kwargs)

    def compress(self, data_list):
        return pickle.dumps(self.initial)
