from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as gen_views

from BoardGameBuddy.common.forms import GameRateForm

from BoardGameBuddy.game.models import Game


#  Games CRUD operations are deliberately
#  delegated to admin (superuser and privileged staff members)
#  - Games are managed from the admin page


class DetailsGame(gen_views.DetailView):
    template_name = 'game-details.html'
    model = Game

    # from common app
    extra_context = {
        'form': GameRateForm(),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if isinstance(self.request.user, AnonymousUser):
            context['user_rated_games_by_pk'] = []
        else:
            context['auth_user'] = self.request.user.buddyprofile
            context['user_rated_games_by_pk'] = [rate.game.pk for rate in
                                                 self.request.user.buddyprofile.gamerating_set.all()]
        return context
