from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from .forms import RegisterUserForm

class UserPermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.pk != kwargs.get('pk'):
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users_list'

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'

class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно изменен'

class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удален'

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index')
    success_message = 'Вы залогинены'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
