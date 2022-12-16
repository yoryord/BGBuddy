from django.core import validators
from django.db import models

from BoardGameBuddy.account.models import BuddyProfile
from BoardGameBuddy.guild.models import BuddyGuild
from BoardGameBuddy.game.models import Game


class GameLike(models.Model):
    buddy = models.ForeignKey(to=BuddyProfile,
                              on_delete=models.CASCADE,
                              )

    game = models.ForeignKey(to=Game,
                             on_delete=models.CASCADE,
                             )


class GameRating(models.Model):
    MIN_RATING = 1.0
    MAX_RATING = 10.0

    rating = models.FloatField(
        validators=(
            validators.MinValueValidator(MIN_RATING, message='Rating could not be lower than 1.0.'),
            validators.MaxValueValidator(MAX_RATING, message='Rating could not be bigger than 10.0.'),

        )
    )

    buddy = models.ForeignKey(to=BuddyProfile,
                              on_delete=models.CASCADE,
                              )

    game = models.ForeignKey(to=Game,
                             on_delete=models.CASCADE,
                             )

    def __str__(self):
        return str(self.rating)


# class GameComment(models.Model):
#     MAX_COMMENT_TEXT = 300
#
#     text = models.TextField(
#         max_length=MAX_COMMENT_TEXT,
#         null=False,
#         blank=False,
#     )
#
#     date_and_time_of_publication = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#     game = models.ForeignKey(
#         Game,
#         on_delete=models.CASCADE,
#     )
#
#     buddy = models.ForeignKey(to=BuddyProfile,
#                               on_delete=models.CASCADE,
#                               )


class GuildMessage(models.Model):
    MAX_GROUP_COMMENT_TEXT = 100

    text = models.TextField(
        max_length=MAX_GROUP_COMMENT_TEXT,
        null=False,
        blank=False,
    )

    date_and_time_of_publication = models.DateTimeField(
        auto_now_add=True,
    )

    # TODO on delete may ne Do Nothing but have to add 'if' statement in the html when user is missing to present 'past user'
    guild = models.ForeignKey(
        BuddyGuild,
        on_delete=models.CASCADE,
    )

    buddy = models.ForeignKey(to=BuddyProfile,
                             on_delete=models.CASCADE,
                             )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-date_and_time_of_publication',]

class RequestJoiningGuild(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True,
    )

    from_buddy = models.ForeignKey(to=BuddyProfile,
                                   on_delete=models.CASCADE,
                                   )
    to_guild = models.ForeignKey(to=BuddyGuild,
                                 on_delete=models.CASCADE,
                                 )

