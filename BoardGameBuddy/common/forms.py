from django import forms

from BoardGameBuddy.common.models import GameRating, GuildMessage


class SearchingForm(forms.Form):
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by guild location ..."
            },

        ),
        label="",
    )


class SearchingGameForm(forms.Form):
    game_title = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by game title ..."
            },

        ),
        label="",
    )


class GameRateForm(forms.ModelForm):
    class Meta:
        model = GameRating
        fields = ('rating',)

        labels = {
            'rating': "",
        }

        help_texts = {
            'rating': "Rates can be between 1.0 and 10.0.",
        }


class GuildMessageForm(forms.ModelForm):
    class Meta:
        model = GuildMessage
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'Add a message ...'
                }
            )
        }
