from django.urls import path

from rooms import views

urlpatterns = [
    path("", views.RoomListView.as_view(), name="room-list"),
    path("<uuid:room_id>/", views.RoomDetailsView.as_view(), name="room-details"),
]
