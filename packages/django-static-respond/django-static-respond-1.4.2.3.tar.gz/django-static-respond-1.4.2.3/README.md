# django-static-respond

Django application contain respond static files.


## Install

```shell
pip install django-static-respond
```

## Settings

```python
    INSTALLED_APPS = [
        ...
        "django_static_respond",
        ...
    ]
```

## Use static resource

```html
{% load staticfiles %}

<script src="{% static "respond/respond.min.js" %}"></script>
```

## About the version

- django-static-respond uses version number like v1.4.2.1.
- The first three number is the version of the respond static files.
- The fourth number is the build number of this package.

## Releases

### v1.4.2.3 2020/09/16

- Depends on nothing.

### v1.4.2.2 2020/03/17

- Remove src folder, use python way to do the package.

### v1.4.2.1 2018/03/28

- First release.