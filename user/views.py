from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
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