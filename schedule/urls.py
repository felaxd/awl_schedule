from django.urls import path
from schedule import views

urlpatterns = [
    path("", views.ScheduleBlockListView.as_view(), name="schedule-block-list"),
    path("<uuid:schedule_block_id>/", views.ScheduleBlockDetailsView.as_view(), name="schedule-block-details"),
]