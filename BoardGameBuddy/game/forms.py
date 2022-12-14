from django import forms

from BoardGameBuddy.game.models import Game


class BaseGameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ('slug',)


class AddGameForm(BaseGameForm):
    class Meta(BaseGameForm.Meta):
        pass


# TODO check and delete redundant
class EditGameForm(BaseGameForm):
    class Meta(BaseGameForm.Meta):
        pass


class RemoveGameForm(BaseGameForm):
    class Meta(BaseGameForm.Meta):
        pass


