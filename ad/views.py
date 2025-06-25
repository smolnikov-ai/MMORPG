from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import (ListView, DetailView, CreateView, )
from .forms import AdvertisementCreateForm
from .models import Advertisement, User


class AdList(ListView):
    model = Advertisement
    ordering = ['-creation_date']
    context_object_name = 'ads'
    template_name = 'ads.html'
    paginate_by = 10

class AdDetail(DetailView):
    model = Advertisement
    context_object_name = 'ad'
    template_name = 'account/base_entrance.html'

class AdCreate(LoginRequiredMixin, CreateView):
#class AdCreate(CreateView):
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


def verify_code(request):
    if request.method == 'POST':
        user_code = request.POST.get('user_code')

        if not user_code or len(user_code.strip()) != 4:
            return render(request, 'account/account_inactive.html',
                          {'error': 'You must enter a verification code that is exactly 4 digits long.'})

        # Проверка существования User с authentication_code равным введенному user_code
        user = User.objects.filter(authentication_code=str(user_code)).first()
        # Если пользователь существует
        if user:

            # Обновляем состояние пользователя
            user.is_active = True
            user.authentication_code = None
            user.save()

            return redirect('/accounts/login/')

        else:
            # Пользователь с данным кодом не найден
            error_message = 'Invalid verification code.'
            return render(request, 'account/account_inactive.html', {'error': error_message})

    else:
        return render(request, 'account/account_inactive.html')
