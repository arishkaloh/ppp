
1. В классе представления редактирования профиля добавьте проверку аутентификации, чтобы пользователь мог редактировать свой профиль только после входа в систему.

python
from django.contrib.auth.mixins import LoginRequiredMixin

class EditProfileView(LoginRequiredMixin, UpdateView):
    ...


2. Настройте пакет allauth в файле конфигурации settings.py. Укажите необходимые параметры, такие как LOGIN_REDIRECT_URL для адреса перенаправления после успешного входа.

python
# settings.py

# Настройки AllAuth
INSTALLED_APPS = [
    ...
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    ...
]

AUTHENTICATION_BACKENDS = [
    ...
    'allauth.account.auth_backends.AuthenticationBackend',
    ...
]

AUTH_USER_MODEL = 'myapp.CustomUser'  # Замените myapp на имя Вашего приложения

LOGIN_REDIRECT_URL = 'home'  # Замените 'home' на имя URL-шаблона для перенаправления после успешного входа

SOCIALACCOUNT_QUERY_EMAIL = True  # Разрешить получение email социальных аккаунтов

ACCOUNT_EMAIL_REQUIRED = True  # Требовать указания email при регистрации

SITE_ID = 1  # Идентификатор сайта

ACCOUNT_EMAIL_VERIFICATION = 'none'  # Отключить подтверждение email

# Настройки для работы с Google-аккаунтом
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}


3. Реализуйте шаблон с формой входа в систему и настройте конфигурацию URL в файле urls.py для обработки этой формы.

python
# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    ...
]


4. Создайте шаблон страницы регистрации пользователей registration.html и настройте конфигурацию URL для обработки этой формы.

python
# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...
    path('register/', auth_views.SignupView.as_view(template_name='registration.html'), name='register'),
    ...
]


5. Реализуйте возможность регистрации через Google-аккаунт, следуя инструкции в документации пакета AllAuth.

python
# settings.py

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}


6. Создайте группы common и authors, путем создания объектов класса Group в вашем коде или через административный интерфейс Django.

python
from django.contrib.auth.models import Group

common_group, created = Group.objects.get_or_create(name='common')
authors_group, created = Group.objects.get_or_create(name='authors')


7. Реализуйте автоматическое добавление новых пользователей в группу common, добавив следующую строку кода в функцию, обрабатывающую создание нового пользователя:

python
new_user.groups.add(common_group)


8. Создайте возможность стать автором, добавив код для добавления пользователя в группу authors:

python
user.groups.add(authors_group)


9. Для группы authors предоставьте права создания и редактирования объектов модели Post (новостей и статей) в административном интерфейсе Django.

python
from django.contrib import admin
from myapp.models import Post

admin.site.register(Post)


10. В классах представлений добавления и редактирования новостей и статей добавьте проверку прав доступа, чтобы только пользователи в группе authors имели возможность выполнять эти действия.

python
from django.contrib.auth.mixins import UserPassesTestMixin

class CreatePostView(UserPassesTestMixin, CreateView):

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    ...


11. Залейте изменения в исходный код в Git-репозиторий для сохранения изменений и контроля версий вашего проекта.

bash
$ git add .
$ git commit -m "Добавлены функции аутентификации, регистрации и проверки прав доступа"
$ git push origin master

