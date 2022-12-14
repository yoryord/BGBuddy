from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic as gen_views

# Create your views here.
from BoardGameBuddy.account.models import BuddyProfile
from BoardGameBuddy.common.forms import SearchingForm, SearchingGameForm, GameRateForm, GuildMessageForm
from BoardGameBuddy.common.models import GameLike, RequestJoiningGuild
from BoardGameBuddy.game.models import Game
from BoardGameBuddy.guild.models import BuddyGuild


def home(request):
    # if request.user.is_authenticated:
    return render(request, "home-page.html")
    # else:
    #     return HttpResponse('Unauthenticated user')


def great_hall(request):
    guilds = BuddyGuild.objects.all()

    search_form = SearchingForm()
    searched_location = ""

    if request.method == "POST":
        search_form = SearchingForm(request.POST)
        if search_form.is_valid():
            searched_location = search_form.cleaned_data['location']
            guilds = guilds.filter(location__icontains=searched_location)

    context = {
        'guilds': guilds,
        'search_form': search_form,
        'searched_location': searched_location
    }

    return render(request, 'common-great-hall.html', context)


class GameInventory(gen_views.ListView):
    template_name = 'common-game-inventory.html'
    model = Game

    extra_context = {
        'game_searching': SearchingGameForm(),

    }

    def get_queryset(self):
        result = super().get_queryset()

        pattern = self.__get_queryset()

        if pattern:
            result = result.filter(title__icontains=pattern)

        return result

    def __get_queryset(self):
        pattern = self.request.GET.get('game_title', None)
        if pattern:
            return pattern.lower()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if isinstance(self.request.user, AnonymousUser):
            context['user_liked_games_by_pk'] = []
        else:

            context['user_liked_games_by_pk'] = [like.game.pk for like in
                                                 self.request.user.buddyprofile.gamelike_set.all()]
        return context


@login_required
def game_like_func(request, pk):
    buddy = request.user.buddyprofile

    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        raise Http404("This game does not exist")

    liked_game = GameLike.objects.filter(buddy=buddy, game=game).first()

    if liked_game:
        liked_game.delete()

    else:
        like = GameLike.objects.create(buddy=buddy, game=game)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f"#game_{pk}")


@login_required
def game_rate(request, pk):
    if request.method == "POST":
        buddy = request.user.buddyprofile
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404("This game does not exist")

        rating_form = GameRateForm(request.POST)
        if rating_form.is_valid():
            rate = rating_form.save(commit=False)
            rate.buddy = buddy
            rate.game = game
            rate.save()

    return redirect(request.META['HTTP_REFERER'] + f"#game_{pk}")


@login_required
def request_joining_guild(request, slug):
    if request.method == "POST":
        buddy = request.user.buddyprofile
        try:
            guild = BuddyGuild.objects.get(slug=slug)
        except BuddyGuild.DoesNotExist:
            raise Http404("This guild does not exist")

        request_joining = RequestJoiningGuild.objects.filter(from_buddy=buddy, to_guild=guild).first()

        # TODO -> change the redirect if need be
        if request_joining:
            return redirect(request.META['HTTP_REFERER'] + f"#guild_{slug}")

        else:
            join_request = RequestJoiningGuild.objects.create(from_buddy=buddy, to_guild=guild)
            join_request.save()

    return redirect(request.META['HTTP_REFERER'] + f"#guild_{slug}")


@login_required
def accept_request(request, pk):
    try:
        join_request = RequestJoiningGuild.objects.get(pk=pk)
    except RequestJoiningGuild.DoesNotExist:
        raise Http404("Wrong request")

    authorised_user = request.user.buddyprofile

    buddy = join_request.from_buddy

    guild = join_request.to_guild

    # TODO specify to redirect to 404
    if not guild.is_admin(authorised_user):
        raise Http404("Wrong way")

    if buddy not in guild.members.all():
        guild.members.add(buddy)

    join_request.delete()

    return redirect(request.META['HTTP_REFERER'])

@login_required
def reject_request(request, pk):
    try:
        join_request = RequestJoiningGuild.objects.get(pk=pk)
    except RequestJoiningGuild.DoesNotExist:
        raise Http404("Wrong request")

    authorised_user = request.user.buddyprofile

    guild = join_request.to_guild

    # TODO specify to redirect to 404
    if not guild.is_admin(authorised_user):
        raise Http404("Wrong way")

    join_request.delete()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def add_message(request, slug):
    if request.method == 'POST':
        try:
            guild = BuddyGuild.objects.filter(slug=slug).get()
        except BuddyGuild.DoesNotExist:
            raise Http404("This guild does not exist")

        authorised_user = request.user.buddyprofile

        if not guild.is_member(authorised_user):
            raise Http404("Wrong way")

        form = GuildMessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.guild = guild
            message.buddy = authorised_user
            message.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def kick_member_from_guild(request, pk, slug):

    try:
        buddy = BuddyProfile.objects.get(pk=pk)
    except BuddyProfile.DoesNotExist:
        raise Http404("Account does not exist")

    try:
        guild = BuddyGuild.objects.get(slug=slug)
    except BuddyGuild.DoesNotExist:
        raise Http404("Guild does not exist")

    authorised_user = request.user.buddyprofile

    if not guild.is_admin(authorised_user):
        raise Http404("Wrong way")

    if buddy in guild.members.all():
        guild.members.remove(buddy)

    return redirect(request.META['HTTP_REFERER'])
