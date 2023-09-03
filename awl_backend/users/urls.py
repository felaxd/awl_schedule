from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

auth_urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

groups_urlpatterns = [
    path("", views.GroupListView.as_view(), name="group-list"),
    path("<int:group_id>/", views.GroupDetailsView.as_view(), name="group-details"),
]

urlpatterns = [
    path("details/", views.UserDetailsView.as_view(), name="user_details"),
]
