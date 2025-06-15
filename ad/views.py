from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView, TemplateView, )
from .forms import AdvertisementCreateForm, UserRegisterForm
from .models import Advertisement


class AdList(ListView):
    model = Advertisement
    ordering = ['-creation_date']
    context_object_name = 'ads'
    template_name = 'ads.html'
    paginate_by = 10

class AdDetail(DetailView):
    model = Advertisement
    context_object_name = 'ad'
    template_name = 'ad.html'

class AdCreate(LoginRequiredMixin, CreateView):
    """
    View-class for creating new advertisement.

    Inherits the LoginRequiredMixin mixins, which guarantees protection from anonymous users
    and verification of necessary permissions.
    The main task of the class is to process the form for creating an advertisement.
    """
    # related Advertisement Model
    model = Advertisement
    # the form class for creating an advertisement
    form_class = AdvertisementCreateForm
    # template for rendering the advertisement creation form
    template_name = 'ad_create.html'

    def form_valid(self, form):
        """
        The method is called when the form is valid (filled out correctly).

        Before saving the record, sets the owner of the ad equal to the current user.
        Overrides the basic implementation of the `form_valid' method to add additional logic.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'user_register.html'

    def form_valid(self, form):
        # создаем экземпляр модели пользователя (User), заполняя его полями из переданной формы (form),
        # но пока не сохраняем объект в базу данных (commit=False)
        user = form.save(commit=False)
        # отключаем активность аккаунта
        user.is_active = False
        # после установки флага неактивности аккаунт сохраняется в базе данных
        user.save()

        # Функционал для отправки письма и генерации токена
        # генерируем уникальный токен, используемый для проверки подлинности процесса активации
        token = default_token_generator.make_token(user)
        # идентификатор пользователя преобразуем в base64 - кодированный формат для безопасной передачи в ссылке
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # Создается обратная ссылка на представление (view) для подтверждения email.
        # Эта ссылка включает закодированный идентификатор пользователя и токен активации.
        activation_url = reverse_lazy('confirm-email', kwargs={'uidb64': uid, 'token': token})
        # Определяем текущий домен веб-сайта, который используется для формирования полной ссылки активации
        current_site = Site.objects.get_current().domain
        # Отправляем письмо пользователю с инструкциями по активации аккаунта и ссылкой для подтверждения.
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'service.notehunter@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('email-confirmation-sent')

class EmailConfirmationSentView(TemplateView):
    template_name = 'email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context

class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email-confirmed')
        else:
            return redirect('email-confirmation-failed')

class EmailConfirmedView(TemplateView):
    template_name = 'email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context

class EmailConfirmationFailedView(TemplateView):
    template_name = 'email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context