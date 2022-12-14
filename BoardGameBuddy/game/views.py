from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as gen_views

from BoardGameBuddy.common.forms import GameRateForm
from BoardGameBuddy.game.forms import AddGameForm, EditGameForm
from BoardGameBuddy.game.models import Game


# TODO - only admin and staff can access this view
class AddGame(LoginRequiredMixin, gen_views.CreateView):
    template_name = 'game-add.html'
    model = Game
    form_class = AddGameForm

    # TODO integration test needed
    def get_success_url(self):
        self.success_url = reverse_lazy('game-details', kwargs={'slug': self.object.slug})
        return super().get_success_url()


class EditGame(LoginRequiredMixin, gen_views.UpdateView):
    template_name = 'game-edit.html'
    model = Game
    form_class = EditGameForm

    # TODO integration test needed
    def get_success_url(self):
        self.success_url = reverse_lazy('game-details', kwargs={'slug': self.object.slug})
        return super().get_success_url()


class RemoveGame(LoginRequiredMixin, gen_views.DeleteView):
    template_name = 'game-remove.html'
    model = Game
    success_url = reverse_lazy('game-inventory')


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
            context['user'] = self.request.user.buddyprofile
            context['user_rated_games_by_pk'] = [rate.game.pk for rate in
                                                 self.request.user.buddyprofile.gamerating_set.all()]
        return context
