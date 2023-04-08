from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup
from .models import User, Group

admin.site.unregister(BaseGroup)


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


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
