============
Django_Param
============
.. image:: https://coveralls.io/repos/github/Aquaveo/django_param/badge.svg

:target: https://coveralls.io/github/Aquaveo/django_param

django_param provides ParamForm class which allows python param to be used in django form.

Quick start
-----------

1. Add 'colorfield', 'django_select2', 'django_param' and 'django.forms' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'colorfield',
        'django_select2',
        'django_param',
    ]


2. Usage:

.. code-block:: python

    # Specify your param class
    class MyParam(param.Parameterized):
        probability = param.Number(0.5, bounds=(0, 1), doc="Probability that...")
        test_string = param.String(default="test string", doc="Your String")

    my_param = MyParam()

    # Initialize Django Form
    django_form = ParamForm({'probability': 0.1, 'test_string': 'test_bound'}, param=my_param)

    # Get data from request.POST
    django_form = ParamForm(request.POST, param=my_param)

    # To return param with values from request.POST
    param = django_form.as_param()


3. Add Form data (assuming your form is named form):

- First you need to add the form media, you can include {{ form.media }} in your header page.
- To add the form, simply use {{ form }}
- you can pass your param to the page and retrieve the values using

.. code-block:: html

    {% for p in param.get_param_values %}
        <li>{{ p.0 }}: {{ p.1 }}</li>
    {% endfor %}


4. Supported Param Class:

- Boolean
- Color
- CalendarDate
- DataFrame
- Date
- FileSelector
- ListSelector
- Magnitude
- MultiFileSelector
- NumericTuple
- ObjectSelector
- Range
- Selector
- String
- Tuple
- XYCoordinates

5. You can also override any default widget with your own custom widget. For example:

.. code-block:: python

    widget_map = {
        param.String:
            lambda parameterized_object, parameter, name: forms.CharField(
                initial=parameterized_object.inspect_value(name) or parameter.default,
                widget=Textarea,
            ),
    }

    form = ParamForm(param=my_param, widget_map=widget_map)
