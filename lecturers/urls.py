from django.urls import path

from lecturers import views

urlpatterns = [
    path("", views.LecturerListView.as_view(), name="lecturer-list"),
    path("<uuid:lecturer_id>/", views.LecturerDetailsView.as_view(), name="lecturer-details"),
]
