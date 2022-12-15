from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as gen_views

from BoardGameBuddy.account.forms import SignUpForm, BuddyProfileEditForm, BuddyPasswordChangeForm
from BoardGameBuddy.account.models import BuddyProfile

UserModel = get_user_model()


class CreateBuddyView(gen_views.CreateView):
    template_name = 'account-register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('account-profile-edit')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields['email'].widget.attrs['placeholder'] = ' Enter email'
        form.fields['password1'].help_text = None
        form.fields['password1'].widget.attrs['placeholder'] = ' Enter password'
        form.fields['password2'].help_text = None
        form.fields['password2'].widget.attrs['placeholder'] = ' Repeat password'

        return form

    # TODO test -> test log in after successful register
    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class BuddyLoginView(auth_views.LoginView):
    template_name = 'account-login.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields['username'].widget.attrs['placeholder'] = ' Enter your email'
        form.fields['password'].widget.attrs['placeholder'] = ' Enter your password'

        return form

    def get_success_url(self):
        return super().get_success_url()


class BuddyLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


# This view uses UserModel and is only accessible by logged in users
# - does not show user_id in the url, they can check their account
class BuddyProfileView(LoginRequiredMixin, gen_views.DetailView):
    template_name = 'account-profile-private.html'
    model = UserModel

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # TODO test -> test plug in for using request pk and do not pass it in url
        self.kwargs["pk"] = request.user.pk


# TODO Account Views
class BuddyProfileEdit(LoginRequiredMixin, gen_views.UpdateView):
    template_name = 'account-profile-edit.html'
    model = BuddyProfile
    form_class = BuddyProfileEditForm
    success_url = reverse_lazy('account-profile')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # TODO test -> test plug in for using request pk and do not pass it in url
        self.kwargs["pk"] = request.user.pk



class BuddyAccountDelete(LoginRequiredMixin, gen_views.DeleteView):
    template_name = 'account-delete.html'
    model = UserModel
    success_url = reverse_lazy('home-page')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # TODO test -> test plug in for using request pk and do not pass it in url
        self.kwargs["pk"] = request.user.pk


class BuddyAccountChangePass(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'account-password-change.html'
    form_class = BuddyPasswordChangeForm
    success_url = reverse_lazy("account-password-change-done")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields['old_password'].help_text = None
        form.fields['old_password'].widget.attrs['placeholder'] = ' Enter old password'
        form.fields['new_password1'].help_text = None
        form.fields['new_password1'].widget.attrs['placeholder'] = ' Enter new password'
        form.fields['new_password2'].help_text = None
        form.fields['new_password2'].widget.attrs['placeholder'] = ' Repeat new password'

        return form


class BuddyAccountChangePassDone(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    template_name = "account-password-change-done.html"


# TODO reset pass
class BuddyAccountResetPass:
    pass


# TODO consider whether LoginRequired is needed here
class BuddyProfileViewPublic(gen_views.DetailView):
    template_name = 'account-profile-public.html'
    model = BuddyProfile
    slug_url_kwarg = 'nickname'
    slug_field = 'nickname'

    def get_queryset(self):
        return super().get_queryset()
