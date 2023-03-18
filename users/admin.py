from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
		"username",
		"first_name",
		"last_name",
		"is_active",
		"is_staff",
		"date_joined",
	)
