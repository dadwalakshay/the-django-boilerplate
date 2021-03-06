from django.db import models


def QUERYSET_VALUES_MONKEY_PATCH(self, *args, **kwargs):
    ################
    # EXPERIMENTAL #
    ################
    # Monkey patch to return Model object with field attributes on calling
    # `qs.values('field_name')` i.e. `qs[0].field_name`
    is_raw = kwargs.pop("raw", False)

    args += tuple(kwargs)

    clone = self._values(*args, **kwargs)

    # Write a custom Iterable class, to implement desired feature.
    # Check below link to Django's source code for reference.
    # https://github.com/django/django/blob/7582d913e7db7f32e4cdcfafc177aa77cbbf4332/django/db/models/query.py#L92
    clone._iterable_class = None if is_raw else models.query.ValuesIterable

    return clone


class BaseManager(models.Manager):
    """Base Manager class to be used with BaseModel class."""

    def __init__(self, *args, **kwargs):
        if models.QuerySet.values is not QUERYSET_VALUES_MONKEY_PATCH:
            models.QuerySet.values = QUERYSET_VALUES_MONKEY_PATCH

        super().__init__(*args, **kwargs)  # noqa
