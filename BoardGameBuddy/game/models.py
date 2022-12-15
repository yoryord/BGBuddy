from datetime import date

from django.core import validators
from django.db import models
from django.utils.text import slugify

from BoardGameBuddy.game.cust_validators import YearRangeValidator, validate_title_chars, \
    validate_first_capital_letter_of_title, validate_publisher_chars


class Game(models.Model):
    MAX_LEN_TITLE = 80
    MIN_LEN_TITLE = 2
    MAX_LEN_DESCRIPTION = 300

    MIN_YEAR = 1980
    MAX_YEAR = int(date.today().strftime("%Y"))
    ERROR_MESSAGE = f'Year must be between {MIN_YEAR} and {MAX_YEAR}.'

    MAX_LEN_GENRE = 20
    GENRE_CHOICES = (
        ('Adventure', 'Adventure'),
        ('Competitive', 'Competitive'),
        ('Cooperative', 'Cooperative'),
        ('Card Game', 'Card Game'),
        ('Dice', 'Dice'),
        ('Educational', 'Educational'),
        ('Economy', 'Economy'),
        ('Fantasy', 'Fantasy'),
        ('Mythology', 'Mythology'),
        ('Management', 'Management'),
        ('Party Game', 'Party Game'),
        ('Racing', 'Racing'),
        ('Science Fiction', 'Science Fiction'),
        ('War Game', 'War Game'),
    )

    MAX_PLAYERS = 10

    MAX_LEN_COMPLEXITY = 15
    COMPLEXITY_CHOICES = (
        ('light', 'light'),
        ('moderate', 'moderate'),
        ('complex', 'complex'),
        ('very complex', 'very complex'),
    )

    MAX_LEN_PUBLISHER = 30

    title = models.CharField(
        max_length=MAX_LEN_TITLE,
        validators=(validators.MinLengthValidator(MIN_LEN_TITLE),
                    validate_first_capital_letter_of_title,
                    validate_title_chars,
                    )
    )

    description = models.TextField(
        max_length=MAX_LEN_DESCRIPTION,
    )

    genre = models.CharField(
        max_length=MAX_LEN_GENRE,
        choices=GENRE_CHOICES,
    )

    release_year = models.IntegerField(
        validators=(YearRangeValidator(MIN_YEAR, MAX_YEAR, ERROR_MESSAGE),)
    )

    max_players = models.PositiveIntegerField(
        validators=(validators.MaxValueValidator(MAX_PLAYERS),)
    )

    complexity = models.CharField(
        max_length=MAX_LEN_COMPLEXITY,
        choices=COMPLEXITY_CHOICES,
    )

    publisher = models.CharField(
        max_length=MAX_LEN_PUBLISHER,
        validators=(validate_publisher_chars,)
    )

    photo_url = models.URLField()

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
            self.slug = slugify(f"{self.title}")

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def get_average_rating(self):
        return self.gamerating_set.aggregate(models.Avg('rating'))['rating__avg']

