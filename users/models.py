from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseDatabaseModel


# Create your models here.
class User(AbstractUser, BaseDatabaseModel):
	def __str__(self) -> str:
		return self.get_full_name()
