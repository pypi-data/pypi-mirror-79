django2-bootstrap3-datetimepicker
=================================

This project was originally a fork of
https://github.com/tutorcruncher/django-bootstrap3-datetimepicker :
The js/css files are now included again into the project

This package uses Bootstrap v3 datetimepicker widget version 2 provided by the following project:
 https://github.com/Eonasdan/bootstrap-datetimepicker

The correct formatting options for dates can be found here:
 http://momentjs.com/docs/

It works only with Bootstrap3.

Install
-------

-  Run ``pip install django2-bootstrap3-datetimepicker``
-  Add ``'bootstrap3_datetime'`` to your ``INSTALLED_APPS``


Example
-------

forms.py
^^^^^^^^

.. code:: python

    from bootstrap3_datetime.widgets import DateTimePicker
    from django import forms

      class ToDoForm(forms.Form):
          todo = forms.CharField(
              widget=forms.TextInput(attrs={"class": "form-control"}))
          date = forms.DateField(
              widget=DateTimePicker(options={"format": "YYYY-MM-DD"}))
          reminder = forms.DateTimeField(
              required=False,
              widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))

The ``options`` will be passed to the JavaScript datetimepicker
instance. Available ``options`` are explained in the following
documents:

-  http://eonasdan.github.io/bootstrap-datetimepicker/

You don't need to set the ``language`` option, because it will be set
the current language of the thread automatically.

template.html
^^^^^^^^^^^^^

.. code:: html

    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet"
                  href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.css">
            <link rel="stylesheet"
                  href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-theme.css">
            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.js">
            </script>
            <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.js">
            </script>
            {{ form.media }}
        </head>
        <body>
            <form method="post" role="form">
                {% for field in form.visible_fields %}
                <div id="div_{{ field.html_name }}"
                     class="form-group{% if field.errors %} has-error{% endif %}">
                    {{ field.label_tag }}
                    {{ field }}
                    <div class="text-muted pull-right">
                        <small>{{ field.help_text }}</small>
                    </div>
                    <div class="help-block">
                        {{ field.errors }}
                    </div>
                </div>
                {% endfor %}
                {% for hidden in form.hidden_fields %}
                    {{ hidden }}
                {% endfor %}
                {% csrf_token %}
                <div class="form-group">
                    <input type="submit" value="Submit" class="btn btn-primary" />
                </div>
            </form>
        </body>
    </html>

Bootstrap3 and jQuery have to be included along with
``{{ form.media }}``

Requirements
------------

-  Python >= 3.4
-  Django >= 2.0
-  Bootstrap == 3.X
-  Moment >= 2.10.6
-  bootstrap-datetimepicker >= 4.15.35

