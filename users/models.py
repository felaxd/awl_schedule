from django.contrib.auth.models import AbstractUser
from common.models import BaseDatabaseModel, ModelDifferenceMixin


# Create your models here.
class User(AbstractUser, BaseDatabaseModel, ModelDifferenceMixin):
	def __str__(self) -> str:
		return self.get_full_name()
