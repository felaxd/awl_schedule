from django.urls import path

from courses import views

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course-list"),
    path("<uuid:course_id>/", views.CourseDetailsView.as_view(), name="course-details"),
    path("<uuid:course_id>/groups/<int:group_id>/", views.CourseGroupsView.as_view(), name="course-groups"),
    path(
        "<uuid:course_id>/lecturers/<uuid:lecturer_id>/", views.CourseLecturersView.as_view(), name="course-lecturers"
    ),
]
