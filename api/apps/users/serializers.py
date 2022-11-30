from apps.users.models import Profile, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ("email", "name")
        read_only_fields = ("email", "name")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("filters", "user")
        read_only_fields = ("user",)
