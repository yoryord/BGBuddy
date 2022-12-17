from django.db import models
from django.utils.text import slugify

from BoardGameBuddy.account.models import BuddyProfile
from BoardGameBuddy.game.models import Game
from BoardGameBuddy.guild.cust_validators import validate_file_size


class BuddyGuild(models.Model):
    MAX_LEN_BAND_NAME = 30
    MAX_LEN_BAND_DESCRIPTION = 300

    MAX_LEN_LOCATION = 50

    guild_name = models.CharField(
        max_length=MAX_LEN_BAND_NAME,
        null=False,
        blank=False,
        unique=True,
    )

    guild_picture = models.ImageField(
        upload_to='mediafiles/guild_photos/',
        validators=(validate_file_size,),
        null=True,
        blank=True,
    )

    guild_description = models.TextField(
        max_length=MAX_LEN_BAND_DESCRIPTION,
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=MAX_LEN_LOCATION,
        null=False,
        blank=False,
    )


    admins = models.ManyToManyField(
        BuddyProfile,
        related_name="admins_set",
        blank=True
    )

    members = models.ManyToManyField(
        BuddyProfile,
        related_name="members_set",
        blank=True
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    list_of_owned_games = models.ManyToManyField(
        Game,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=False,
    )

    def save(
            self, *args, **kwargs
    ):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.guild_name}")

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.guild_name

    class Meta:
        ordering = ['guild_name',]

    def is_admin(self, obj):
        if obj not in self.admins.all():
            return False
        return True

    def is_member(self, obj):
        if obj not in self.members.all():
            return False
        return True

    def promote_admin(self, obj):
        self.admins.add(obj)
