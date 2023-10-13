from django.db import models

from common.models import BaseDatabaseModel, TimestampMixin


# Create your models here.
class Room(BaseDatabaseModel, TimestampMixin):
    name = models.CharField(max_length=32)
    is_public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
