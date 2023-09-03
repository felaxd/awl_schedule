from django.contrib import admin

from rooms.models import Room


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
