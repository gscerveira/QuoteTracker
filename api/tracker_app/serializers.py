from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Item, Project, Store

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Serializes and deserializes User objects to and from JSON.
    Provides validation for email, username and password fields.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], max_length=255
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())], max_length=255
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "validators": [validate_password]},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """
        Create a new User instance.

        Args:
            validated_data (dict): Validated data for creating a new User.

        Returns:
            User: The created User instance.
        """
        user = User.objects.create_user(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Serializes and deserializes login credentials to and from JSON.
    """

    username = serializers.CharField()
    password = serializers.CharField()


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.

    Serializes and deserializes Project objects to and from JSON.
    """

    class Meta:
        model = Project
        fields = ["id", "user", "name", "description"]
        extra_kwargs = {"user": {"read_only": True}}


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Item model.

    Serializes and deserializes Item objects to and from JSON.
    """

    class Meta:
        model = Item
        fields = ["id", "project", "name", "status", "store", "description"]


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Store model.

    Serializes and deserializes Store objects to and from JSON.
    """

    class Meta:
        model = Store
        fields = ["id", "name", "user"]
        extra_kwargs = {"user": {"read_only": True}}
