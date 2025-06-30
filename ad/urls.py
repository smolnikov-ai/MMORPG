from django.urls import path
from .views import (AdList, AdCreate, advertisement_detail, accept_reply, RepliesRequestUser, )


urlpatterns = [
    # all user advertisements
    path('ad/', AdList.as_view(), name='ad-list'),
    # details of the advertisement by pk
    path('ad/<int:pk>/', advertisement_detail, name='ad-detail'),
    # creating a new advertisement
    path('ad/create/', AdCreate.as_view(), name='ad-create'),
    path('reply/<int:pk>/', accept_reply, name='accept-reply'),
    path('ad/user/', RepliesRequestUser.as_view(), name='reply-ad-user'),
]
