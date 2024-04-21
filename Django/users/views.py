from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UpdateProfileForm


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    model = User
    success_url = reverse_lazy('home')

    def form_valid(self, form: UserRegisterForm):
        res = super().form_valid(form)
        login(self.request, form.instance)
        return res


class LoginView(DjangoLoginView):
    template_name = 'login.html'
    form_class = UserLoginForm


class LogoutView(DjangoLogoutView):
    pass


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'
    form_class = UpdateProfileForm
    model = User
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)
