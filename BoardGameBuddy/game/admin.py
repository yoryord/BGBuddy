from django.contrib import admin

from BoardGameBuddy.game.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", 'publisher', "genre", 'release_year', 'max_players', 'complexity')
    list_filter = ("title", "publisher", "release_year", 'max_players', 'complexity')
    search_fields = ("title", "publisher", "release_year", 'max_players', 'complexity' )
    ordering = ("title",)


# title
# genre
# release_year
# max_players
# complexity
# publisher
# slug