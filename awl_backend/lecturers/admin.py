from django.contrib import admin

from lecturers.models import Lecturer


# Register your models here.
@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "_first_name",
        "title",
        "job_position",
    )
    search_fields = ("first_name", "last_name", "contact_email")

    def _first_name(self, obj: Lecturer) -> str:
        return obj.first_name or "-"
