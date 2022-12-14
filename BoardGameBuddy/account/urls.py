from django.urls import path

from BoardGameBuddy.account.views import CreateBuddyView, BuddyLogoutView, BuddyLoginView, BuddyProfileView, \
    BuddyProfileEdit, BuddyAccountDelete, BuddyAccountChangePass, BuddyAccountChangePassDone, BuddyProfileViewPublic

urlpatterns = [
    path('register/', CreateBuddyView.as_view(), name='account-register'),
    path('login/', BuddyLoginView.as_view(), name='account-login'),
    path('logout/', BuddyLogoutView.as_view(), name='account-logout'),
    path('profile/', BuddyProfileView.as_view(), name='account-profile'),
    path('profile/edit/', BuddyProfileEdit.as_view(), name='account-profile-edit'),
    path('profile/change-password/', BuddyAccountChangePass.as_view(), name='account-password-change'),
    path('profile/change-password/done/', BuddyAccountChangePassDone.as_view(), name='account-password-change-done'),
    path('profile/delete/', BuddyAccountDelete.as_view(), name='account-delete'),
    # slug is filled with nickname
    path('profile/pub/<slug:nickname>/', BuddyProfileViewPublic.as_view(), name='account-profile-public'),
]

from .signals import *
