from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (AdList, AdDetail, AdCreate, verify_code, )


urlpatterns = [
    # all user advertisements
    path('ad/', AdList.as_view(), name='ad-list'),
    # details of the advertisement by pk
    path('ad/<int:pk>/', AdDetail.as_view(), name='ad-detail'),
    # creating a new advertisement
    path('ad/create/', AdCreate.as_view(), name='ad-create'),
    path('verify/', verify_code, name='verify-code'),
]
