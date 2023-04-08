from django.contrib import admin

from schedule.models import Schedule, ScheduleBlock, LecturerScheduleBlockThrough


# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "progress", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)


class LecturerScheduleBlockThroughInline(admin.TabularInline):
    model = LecturerScheduleBlockThrough
    extra = 0


@admin.register(ScheduleBlock)
class ScheduleBlockAdmin(admin.ModelAdmin):
    list_display = ("course_name", "type", "start", "end", "get_groups", "get_lecturers", "created_at")
    list_filter = ("groups", "lecturers", "rooms")
    search_fields = ("course_name", "groups__name", "lecturers__first_name", "lecturers__last_name", "rooms__name")
    filter_horizontal = ("groups", "rooms")
    inlines = (LecturerScheduleBlockThroughInline,)

    def get_groups(self, obj: ScheduleBlock) -> str:
        return ", ".join(obj.groups.values_list("name", flat=True))

    get_groups.short_description = "groups"

    def get_lecturers(self, obj: ScheduleBlock) -> str:
        return ", ".join([f"{lecturer}" for lecturer in obj.lecturers.all()])

    get_lecturers.short_description = "lecturers"
