from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db import models

from common.models import BaseDatabaseModel, ModelDifferenceMixin, TimestampMixin


# Create your models here.
class User(AbstractUser, BaseDatabaseModel, ModelDifferenceMixin):
	def __str__(self) -> str:
		return self.get_full_name()


class Group(BaseGroup, BaseDatabaseModel, TimestampMixin, ModelDifferenceMixin):
	is_public = models.BooleanField(default=False)

