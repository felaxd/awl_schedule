from typing import Any, List
from uuid import UUID

from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, URLPattern, path
from django.utils.html import format_html

from common.container import container
from schedule.models import Schedule, ScheduleBlock, LecturerScheduleBlockThrough


class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule
        help_texts = {
            "name": "Nazwa planu (nie wyświetlana)",
            "file": "Plik excel",
            "year": "Rok na jaki jest plan",
            "month": "Miesiąc na jaki jest plan",
            "worksheet_name": "Nazwa arkusza w pliku",
            "errors": "Wykryte błędy w pliku",
            "replaced_schedule_blocks": "Bloczki które zostały zamienione",
            "schedule_blocks": "Wykryte nowe bloczki",
            "lecturers": "Wykryci nowi prowadzący",
            "rooms": "Wykryte nowe sale",
            "groups": "Wykryte nowe grupy",
            "courses": "Wykryte nowe przedmioty",
        }
        exclude = ()


# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm
    list_display = ("name", "status", "progress", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
    filter_horizontal = (
        "replaced_schedule_blocks",
        "schedule_blocks",
        "lecturers",
        "groups",
        "rooms",
        "courses",
    )
    readonly_fields = ("status", "progress", "schedule_actions",)

    def schedule_actions(self, obj: Schedule) -> str:
        actions = []
        if obj.status == "NEW":
            actions.append(
                f'<a class="button" href="{reverse("admin:schedule-init-excel", args=[obj.id])}">Pobierz z pliku</a>'
            )
        elif obj.status in ["FINISHED", "REVERTED"]:
            actions.append(
                f'<a class="button" href="{reverse("admin:schedule-publicate", args=[obj.id])}">Opublikuj</a>'
            )
        elif obj.status == "PUBLICATED":
            actions.append(
                f'<a class="button" href="{reverse("admin:schedule-revert", args=[obj.id])}">Cofnij publikacje</a>'
            )
        return format_html(" ".join(actions))

    schedule_actions.short_description = "akcje"

    def _process_init_excel(
        self, request: HttpRequest, schedule_id: UUID, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        schedule: Schedule = self.get_object(request, schedule_id)  # type: ignore
        if schedule:
            try:
                container().schedule_service.update_schedule_from_excel(schedule)
                self.message_user(request, f"Pobrano plan z pliku {schedule.file}!", level=messages.INFO)
            except Exception as ex:
                self.message_user(request, f"Błąd! [{ex}]", level=messages.ERROR)
        return HttpResponseRedirect(
            reverse(
                "admin:schedule_schedule_change", current_app=self.admin_site.name, kwargs={"object_id": schedule.id}
            )
        )

    def _process_publication(
        self, request: HttpRequest, schedule_id: UUID, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        schedule: Schedule = self.get_object(request, schedule_id)  # type: ignore
        if schedule:
            container().schedule_service.publicate_schedule(schedule)
            self.message_user(request, f"Opublikowano {schedule.name}!", level=messages.INFO)
        return HttpResponseRedirect(
            reverse(
                "admin:schedule_schedule_change", current_app=self.admin_site.name, kwargs={"object_id": schedule.id}
            )
        )

    def _process_revert(
        self, request: HttpRequest, schedule_id: UUID, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        schedule: Schedule = self.get_object(request, schedule_id)  # type: ignore
        if schedule:
            container().schedule_service.revert_schedule_publication(schedule)
            self.message_user(request, f"Cofnięto publickacje {schedule.name}!", level=messages.WARNING)
        return HttpResponseRedirect(
            reverse(
                "admin:schedule_schedule_change", current_app=self.admin_site.name, kwargs={"object_id": schedule.id}
            )
        )

    def get_urls(self) -> List[URLPattern]:
        urls = super().get_urls()
        custom_urls = [
            path(
                "<uuid:schedule_id>/excel-init/",
                self.admin_site.admin_view(self._process_init_excel),
                name="schedule-init-excel",
            ),
            path(
                "<uuid:schedule_id>/publicate/",
                self.admin_site.admin_view(self._process_publication),
                name="schedule-publicate",
            ),
            path(
                "<uuid:schedule_id>/revert/",
                self.admin_site.admin_view(self._process_revert),
                name="schedule-revert",
            ),
        ]
        return custom_urls + urls


class LecturerScheduleBlockThroughInline(admin.TabularInline):
    model = LecturerScheduleBlockThrough
    extra = 0


@admin.register(ScheduleBlock)
class ScheduleBlockAdmin(admin.ModelAdmin):
    list_display = ("course_name", "type", "start", "end", "get_groups", "get_lecturers", "is_public", "created_at")
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
