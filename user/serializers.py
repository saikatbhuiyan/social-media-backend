from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
  """Serializers registration requests and creates a new user."""
  # Ensure passwords are at least 8 characters long, no longer than 128
  # characters, and can not be read by the client.
  password = serializers.CharField(
    max_length=128,
    min_length=4,
    write_only=True
  )
  # The client should not be able to send a token along with a registration
  # request. Making `token` read-only handles that for us.
  token = serializers.CharField(max_length=255, read_only=True)

  class Meta:
    model = User
    # List all of the fields that could possibly be included in a request
    # or response, including fields specified explicitly above.
    fields = ['email', 'username', 'password', 'token']

  def create(self, validated_data):
  # Use the `create_user` method we wrote earlier to create a new user.
    return User.objects.create_user(**validated_data)


