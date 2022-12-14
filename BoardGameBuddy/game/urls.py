from django.urls import path

from BoardGameBuddy.game.views import AddGame, EditGame, RemoveGame, DetailsGame
#TODO to add create and edit templates accessible only by is_staff users
urlpatterns = [
    path('add/', AddGame.as_view(), name='game-add'),
    path('edit/<slug:slug>', EditGame.as_view(), name='game-edit'),
    path('remove/<slug:slug>', RemoveGame.as_view(), name='game-remove'),
    path('details/<slug:slug>', DetailsGame.as_view(), name='game-details'),

]
