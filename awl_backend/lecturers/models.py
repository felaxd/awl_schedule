from django.db import models
from common.models import BaseDatabaseModel, TimestampMixin, ModelDifferenceMixin


class Lecturer(BaseDatabaseModel, TimestampMixin, ModelDifferenceMixin):
	
	first_name = models.CharField(max_length=128)
	last_name = models.CharField(max_length=128)
	title = models.CharField(max_length=128, blank=True)
	job_position = models.CharField(max_length=128, blank=True)
	contact_email = models.CharField(max_length=128, blank=True)
	is_public = models.BooleanField(default=False)

	def __str__(self) -> str:
		return " ".join([self.title, self.first_name, self.last_name])
