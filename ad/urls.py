from django.urls import path
from .views import (AdList, AdCreate, advertisement_detail, )


urlpatterns = [
    # all user advertisements
    path('ad/', AdList.as_view(), name='ad-list'),
    # details of the advertisement by pk
    path('ad/<int:pk>/', advertisement_detail, name='ad-detail'),
    # creating a new advertisement
    path('ad/create/', AdCreate.as_view(), name='ad-create'),
    #path('acceptreply/', accept_reply, name='accept-reply'),
]
