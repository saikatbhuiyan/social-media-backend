from django.urls import path

from .views import LoginAPIView, RegistrationAPIView

app_name = 'user'

urlpatterns = [
  path('users/', RegistrationAPIView.as_view()),
  path('login/', LoginAPIView.as_view()),
]