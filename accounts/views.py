from django.shortcuts import render, redirect

from ad.models import User


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

            return redirect('/account/login/')

        else:
            # Пользователь с данным кодом не найден
            error_message = 'Invalid verification code.'
            return render(request, 'account/account_inactive.html', {'error': error_message})

    else:
        return render(request, 'account/account_inactive.html')
