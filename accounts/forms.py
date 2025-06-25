import random

from allauth.account.forms import SignupForm
from django.core.mail import send_mail

from MMORPG import settings


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