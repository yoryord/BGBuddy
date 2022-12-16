from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import mixins as auth_mixins

from django.contrib.auth.models import AnonymousUser

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as gen_views

from BoardGameBuddy.common.forms import GuildMessageForm
from BoardGameBuddy.common.models import RequestJoiningGuild
from BoardGameBuddy.guild.admin_access_mixin import AdminAccessMixin
from BoardGameBuddy.guild.forms import CreateGuildForm, EditGuildForm
from BoardGameBuddy.guild.models import BuddyGuild


class BaseGuildView(auth_mixins.LoginRequiredMixin, gen_views.ListView):
    template_name = 'guild-base.html'
    model = BuddyGuild
    context_object_name = 'guilds'

    def get_queryset(self):

        queryset = super().get_queryset()

        buddy = self.request.user.buddyprofile
        # TODO test exclusion of the queryset when buddy is not in certain guld
        for query in queryset:
            if buddy not in query.members.all():
                queryset = queryset.exclude(pk=query.pk)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buddy'] = self.request.user.buddyprofile

        return context


class CreateGuild(auth_mixins.LoginRequiredMixin, gen_views.CreateView):
    template_name = 'guild-create.html'
    model = BuddyGuild
    form_class = CreateGuildForm

    def form_valid(self, form):
        result = super().form_valid(form)

        buddy = self.request.user.buddyprofile
        self.object.admins.add(buddy)
        self.object.members.add(buddy)

        self.object.save()

        return result

    # TODO integration test needed
    def get_success_url(self):
        self.success_url = reverse_lazy('details-guild', kwargs={'slug': self.object.slug})
        return super().get_success_url()


class EditGuild(auth_mixins.LoginRequiredMixin, AdminAccessMixin, gen_views.UpdateView):
    template_name = 'guild-edit.html'
    model = BuddyGuild
    form_class = EditGuildForm

    def render_to_response(self, context, **response_kwargs):
        self.admin_check(context)
        return super().render_to_response(context, **response_kwargs)

    # TODO integration test needed
    def get_success_url(self):
        self.success_url = reverse_lazy('details-guild', kwargs={'slug': self.object.slug})
        return super().get_success_url()


class DeleteGuild(auth_mixins.LoginRequiredMixin, AdminAccessMixin, gen_views.DeleteView):
    template_name = 'guild-delete.html'
    model = BuddyGuild
    success_url = reverse_lazy('common-grate-hall')

    def render_to_response(self, context, **response_kwargs):
        self.admin_check(context)
        return super().render_to_response(context, **response_kwargs)

    def get_success_url(self):
        return super().get_success_url()

class DetailsGuild(gen_views.DetailView):
    template_name = 'guild-details.html'
    model = BuddyGuild

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        guild = self.object

        if isinstance(self.request.user, AnonymousUser):
            context['join_request'] = False
            context['is_member'] = False
            context['is_admin'] = False

        else:
            buddy = self.request.user.buddyprofile
            guild_messages = guild.guildmessage_set.all()

            join_request = RequestJoiningGuild.objects.filter(from_buddy=buddy, to_guild=guild).first()

            context['join_request'] = join_request
            context['is_member'] = guild.is_member(buddy)
            context['is_admin'] = guild.is_admin(buddy)
            context['message_form'] = GuildMessageForm()
            context['guild_messages'] = guild_messages

        context['members'] = guild.members.all()

        return context



class GuildMasterView(auth_mixins.LoginRequiredMixin, AdminAccessMixin, gen_views.DetailView):
    template_name = 'guild_master.html'
    model = BuddyGuild

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        guild = self.object

        join_requests = RequestJoiningGuild.objects.filter(to_guild=guild)

        context['join_requests'] = join_requests
        context['members'] = guild.members.all()
        context['admins'] = guild.admins.all()

        return context

    def render_to_response(self, context, **response_kwargs):
        self.admin_check(context)
        return super().render_to_response(context, **response_kwargs)


@login_required
def leave_guild(request, slug):
    try:
        guild = BuddyGuild.objects.get(slug=slug)
    except BuddyGuild.DoesNotExist:
        raise Http404("This guild does not exist")

    buddy = request.user.buddyprofile

    if guild.is_member(buddy):
        guild.members.remove(buddy)
    if guild.is_admin(buddy):
        guild.admins.remove(buddy)

    # when the admin leaves, below assigns new admin if available or deletes the guld
    if guild.admins.count() == 0:
        if guild.members.count() == 0:
            guild.delete()
        else:
            first_buddy = guild.members.first()
            guild.promote_admin(first_buddy)

    return redirect('home-page')



