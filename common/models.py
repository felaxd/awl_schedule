import uuid
from typing import Any

from django.db import models
from django.forms import model_to_dict


class BaseDatabaseModel(models.Model):
    """BaseModel used across all database models"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")

    ADD_PERMISSION_CODENAME: str
    CHANGE_PERMISSION_CODENAME: str
    DELETE_PERMISSION_CODENAME: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.ADD_PERMISSION_CODENAME = f"{self._meta.app_label}.add_{self._meta.model_name}"
        self.CHANGE_PERMISSION_CODENAME = f"{self._meta.app_label}.change_{self._meta.model_name}"
        self.DELETE_PERMISSION_CODENAME = f"{self._meta.app_label}.delete_{self._meta.model_name}"
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """Provides created_at and updated_at fields, that will be automatically tracked"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelDifferenceMixin(models.Model):
    """
    A model mixin that tracks model fields values and provide some useful api to know what fields have been changed.
    """
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ModelDifferenceMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        current = self._dict
        diffs = [(k, (v, current[k])) for k, v in self.__initial.items() if v != current[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return list(self.diff.keys())

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDifferenceMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])
