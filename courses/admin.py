from django.contrib import admin

from courses.models import Course, LecturerCourseThrough, GroupCourseThrough


class GroupCourseThroughInline(admin.TabularInline):
    model = GroupCourseThrough
    extra = 0


class LecturerCourseThroughInline(admin.TabularInline):
    model = LecturerCourseThrough
    extra = 0


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (GroupCourseThroughInline, LecturerCourseThroughInline)
    search_fields = ("name",)
    list_filter = ("lecturers", "groups")
