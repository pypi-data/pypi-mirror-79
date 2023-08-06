from django import forms
import pandas as pd


class DataFrameWidget(forms.Widget):
    template_name = 'django_param/dataframe/dataframe.html'

    class Media:
        css = {'all': ('django_param/dataframe/dataframe.css',)}
        js = [
            'django_param/dataframe/dataframe.js',
        ]

    def get_context(self, name, value, attrs):
        context = {}
        # Get columns
        dataframe_prefix = f"___{name}__"
        columns = [col.replace(dataframe_prefix, "") for col in value.columns]
        row_values = value.values.tolist()
        # Get rows
        rows = list()
        for row_value in row_values:
            rows.append(dict(zip(columns, row_value)))

        context['widget'] = {
            'name': name,
            'dataframe_prefix': dataframe_prefix,
            'is_hidden': self.is_hidden,
            'required': self.is_required,
            'value': value.to_html(),
            'columns': columns,
            'rows': rows,
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name,
        }
        return context

    def value_from_datadict(self, data, files, name):
        """
        convert values into dataframe object.
        """
        data_dict = {}
        for key, value in data.items():
            if key[-2:] == "__":
                data_dict[key.replace("___" + name + "__", "")] = data.getlist(key)
        dataframe = pd.DataFrame.from_dict(data_dict)

        return dataframe
