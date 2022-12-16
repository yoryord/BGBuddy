from django.urls import path

from BoardGameBuddy.game.views import DetailsGame

#  Games CRUD operations are deliberately
#  delegated to admin (superuser and privileged staff members)
#  - Games are managed from the admin page


urlpatterns = [
    path('details/<slug:slug>', DetailsGame.as_view(), name='game-details'),
]
