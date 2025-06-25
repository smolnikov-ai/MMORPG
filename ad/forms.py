import random

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from MMORPG import settings
from .models import Advertisement, Reply


class AdvertisementForm(forms.ModelForm):
    '''
    The advertisement form based on the model Advertisement

    The form fields include:
        title (str): title of the advertisement
        content (RichTextUploadingField): advertisement content with visual editor support
        category (str): category of the advertisement

    Attributes:
        content (forms.CharField): a field for entering the content of an ad with a visual editor widget
    '''
    content = forms.CharField()

    class Meta:
        '''
        Metadata of the form

        Fields:
            title (str): title of the advertisement
            content (RichTextUploadingField): content of the advertisement
            category (str): category of the advertisement
        '''
        model = Advertisement
        fields = [
            'title',
            'content',
            'category',
        ]


class ReplyForm(forms.ModelForm):
    '''
    The reply form based on the model Reply

    The form fields include:
        content (str): content of the reply
    '''

    class Meta:
        '''
        Metadata of the form

        Fields:
            content (str): content of the reply
        '''
        model = Reply
        fields = [
            'content',
        ]


class AdvertisementCreateForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            'title',
            'content',
            'category',
        ]


class AccountSignupForm(SignupForm):

    def save(self, request):
        # Получаем экземпляр пользователя, созданный базовой формой
        user = super().save(request)

        # генерируем код аутентификации
        authentication_code = random.randrange(1000, 10000)

        # задаем пользователю authentication_code
        user.authentication_code = authentication_code

        # Устанавливаем пользователя в состояние 'inactive'
        user.is_active = False
        user.save()

        message = f'To authenticate, enter this code {authentication_code} on the website.'
        email = user.email

        send_mail(
            subject='Confirmation of registration.',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return user


    # def authentication(self, request):
    #     if request.method == 'POST':
    #
    #         # генерируем код аутентификации
    #         authentication_code = generate_random_code()
    #
    #         # перехватываем user через pk, заполняем его поле authentication_code и делаем user неактивным
    #         user_pk = request.POST.get('user_pk')
    #         if user_pk:
    #             try:
    #                 user = User.objects.get(pk=user_pk)
    #                 user.authentication_code = authentication_code
    #
    #                 user.is_active = False
    #                 user.save()
    #             except User.DoesNotExist:
    #                 return HttpResponseBadRequest("Пользователь не найден.")
    #
    #
    #
    #         email = request.POST.get('email')
    #         message = f'To authenticate, enter this code {authentication_code} on the website.'
    #
    #         send_mail(
    #             subject='Confirmation of registration.',
    #             message=message,
    #             from_email=settings.DEFAULT_FROM_EMAIL,
    #             recipient_list=[email],
    #             fail_silently=False,
    #         )
    #         return None
    #     return None