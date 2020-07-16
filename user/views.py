from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
  LoginSerializer, RegistrationSerializer
)
from .renderers import UserJSONRenderer

class RegistrationAPIView(APIView):
  # Allow any user (authenticated or not) to hit this endpoint.
  permission_classes = (AllowAny,)
  serializer_class = RegistrationSerializer
  # renderer_classes = (UserJSONRenderer,)

  def post(self, request):
    user = request.data.get('user', {})
    # The create serializer, validate serializer, save serializer pattern
    # below is common and you will see it a lot throughout this course and
    # your own work later on. Get familiar with it.
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
  permission_classes = (AllowAny,)
  renderer_classes = (UserJSONRenderer,)
  serializer_class = LoginSerializer

  def post(self, request):
    user = request.data.get('user', {})
    # Notice here that we do not call `serializer.save()` like we did for
    # the registration endpoint. This is because we don't have
    # anything to save. Instead, the `validate` method on our serializer
    # handles everything we need.
    serializer = self.serializer_class(data=user)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)