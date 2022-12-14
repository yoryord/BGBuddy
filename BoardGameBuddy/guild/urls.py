from django.urls import path

from BoardGameBuddy.guild.views import CreateGuild, EditGuild, DeleteGuild, DetailsGuild, BaseGuildView, \
    GuildMasterView, leave_guild

urlpatterns = [
    path('', BaseGuildView.as_view(), name='base-guild'),
    path('create/', CreateGuild.as_view(), name='create-guild'),
    path('edit/<slug:slug>/', EditGuild.as_view(), name='edit-guild'),
    path('delete/<slug:slug>/', DeleteGuild.as_view(), name='delete-guild'),
    path('<slug:slug>', DetailsGuild.as_view(), name='details-guild'),
    path('leave/<slug:slug>', leave_guild, name='leave-guild'),
    path('<slug:slug>/master/', GuildMasterView.as_view(), name='guild-master-board'),

]
