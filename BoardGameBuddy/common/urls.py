from django.urls import path

from BoardGameBuddy.common.views import home, great_hall, game_like_func, GameInventory, game_rate, \
    request_joining_guild, accept_request, reject_request, add_message, kick_member_from_guild

urlpatterns = [
    path('', home, name='home-page'),
    path('great-hall/', great_hall, name='common-grate-hall'),
    path('games/like/<int:pk>/', game_like_func, name='game-like'),
    path('games/rate/<int:pk>/', game_rate, name='game-rate'),
    path('games/', GameInventory.as_view(), name='game-inventory'),
    path('guild/request/<slug:slug>', request_joining_guild, name='request-joining-guild'),
    path('guild/request/<int:pk>/accept', accept_request, name='request-accept'),
    path('guild/request/<int:pk>/reject', reject_request, name='request-reject'),
    path('guild/comment/<slug:slug>', add_message, name='guild-message'),
    path('guild/kick/<int:pk>/<slug:slug>', kick_member_from_guild, name='kick-from-guild'),

]