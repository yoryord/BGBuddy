from django.contrib import admin

from BoardGameBuddy.guild.models import BuddyGuild


@admin.register(BuddyGuild)
class GuildAdmin(admin.ModelAdmin):
    pass
