from django.urls import path

from .views import verify_code

urlpatterns = [
    path('verify/', verify_code, name='verify-code'),
]