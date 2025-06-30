from django.urls import path
from .views import (AdList, AdCreate, advertisement_detail, accept_reply, delete_reply, RepliesRequestUser, AdEdit, )


urlpatterns = [
    # all user advertisements
    path('ad/', AdList.as_view(), name='ad-list'),
    # details of the advertisement by pk
    path('ad/<int:pk>/', advertisement_detail, name='ad-detail'),
    path('ad/<int:pk>/edit/', AdEdit.as_view(), name='ad-edit'),
    # creating a new advertisement
    path('ad/create/', AdCreate.as_view(), name='ad-create'),
    path('reply/<int:pk>/', accept_reply, name='accept-reply'),
    path('reply/delete/<int:pk>/', delete_reply, name='delete-reply'),
    path('ad/user/', RepliesRequestUser.as_view(), name='reply-ad-user'),
]
