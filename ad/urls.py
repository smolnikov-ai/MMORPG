from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (AdList, AdDetail, AdCreate, UserRegisterView, EmailConfirmedView, EmailConfirmationSentView,
                    UserConfirmEmailView, EmailConfirmationFailedView)


urlpatterns = [
    # all user advertisements
    path('ad/', AdList.as_view(), name='ad-list'),
    # details of the advertisement by pk
    path('ad/<int:pk>/', AdDetail.as_view(), name='ad-detail'),
    # creating a new advertisement
    path('ad/create/', AdCreate.as_view(), name='ad-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email-confirmation-sent'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email-confirmed'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm-email'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

]
