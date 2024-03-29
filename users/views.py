import random

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView, TemplateView

from config import settings
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main:mailing-list')

    def form_valid(self, form):
        user = form.save()

        current_site = self.request.get_host()
        subject = 'Подтверждение регистрации'

        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        user.verification_code = verification_code

        if user.is_staff:
            manager_group = Group.objects.get(name='Manager')
            user.groups.add(manager_group)

        user.save()

        message = render_to_string('registration/activation_email.html', {
            'user': user,
            'domain': current_site,
            'verification_code': verification_code
        })

        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])

        user.is_verified = True
        user.is_active = True
        user.save()

        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('main:mailing-list')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ConfirmRegister(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/register_done.html')

    def post(self, request, *args, **kwargs):
        token = int(request.POST.get('verification_code'))
        user = get_object_or_404(User, verification_code=token)

        if not user.is_active:
            user.is_active = True
            user.save()
            return redirect('users:login')
        return redirect('main:mailing-list')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        new_password = get_random_string(length=12)

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        send_mail(
            subject='Заявка на изменение пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)

    class UserPasswordResetView(PasswordResetView):
        template_name = 'registration/password_reset_form.html'
        success_url = reverse_lazy('users:password_reset_done')
        form_class = PasswordResetForm

        def form_valid(self, form):
            email = form.cleaned_data['email']
            user = get_user_model().objects.get(email=email)
            uid = str(user.pk)
            token = user.verification_code

            subject = 'Сброс пароля'
            message = 'Чтобы завершить сброс пароля, перейдите по ссылке: {url}'.format(
                url=self.request.build_absolute_uri(
                    reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
            )
            from_email = EMAIL_HOST_USER
            send_mail(subject, message, from_email, [email])

            return super().form_valid(form)

        def get_success_url(self):
            return reverse('users:password-reset')

    def get_success_url(self):
        return reverse('users:password_reset')


class UserPasswordResetDoneView(LoginRequiredMixin, PasswordResetDoneView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/password_reset_done.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetConfirmView(LoginRequiredMixin, PasswordResetConfirmView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_confirm')


class UserPasswordResetCompleteView(LoginRequiredMixin, PasswordResetCompleteView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/password_reset_done.html'
    success_url = reverse_lazy('users:password_reset_done')
