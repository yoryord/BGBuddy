from django import forms

from BoardGameBuddy.guild.models import BuddyGuild


class BaseGuildForm(forms.ModelForm):
    class Meta:
        model = BuddyGuild
        exclude = ('admins', 'members', 'created_on',)


class CreateGuildForm(BaseGuildForm):
    class Meta(BaseGuildForm.Meta):
        pass


class EditGuildForm(BaseGuildForm):
    class Meta(BaseGuildForm.Meta):
        pass
