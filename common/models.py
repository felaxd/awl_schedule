import uuid

from django.db import models


class BaseDatabaseModel(models.Model):
    """BaseModel used across all database models"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """Provides created_at and updated_at fields, that will be automatically tracked"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
