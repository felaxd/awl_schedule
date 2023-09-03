from users.models import Group
from rest_framework import serializers

from users.models import User


# Create your views here.
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "last_login",
        )
        read_only_fields = (
            "id",
            "username",
            "last_login",
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "name",
        )
