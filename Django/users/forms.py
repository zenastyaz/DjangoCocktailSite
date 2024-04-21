from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, UsernameField
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Электронная почта"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))
    username = UsernameField(widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class UpdateProfileForm(UserChangeForm):
    username = UsernameField(disabled=True)
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name'
        ]


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
