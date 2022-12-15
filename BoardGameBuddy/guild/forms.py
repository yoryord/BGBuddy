from django import forms

from BoardGameBuddy.guild.models import BuddyGuild


class BaseGuildForm(forms.ModelForm):
    class Meta:
        model = BuddyGuild
        exclude = ('admins', 'members', 'created_on',)


class CreateGuildForm(BaseGuildForm):
    class Meta(BaseGuildForm.Meta):
        labels = {
            'guild_name': "",
            'guild_description': "",
            'location': "",
            'guild_picture': "Guild Photo",
        }

        widgets ={
            'guild_name': forms.TextInput(
                attrs={
                    'placeholder': "Guild name"
                }
            ),
            'guild_description': forms.TextInput(
                attrs={
                    'placeholder': "Guild description"
                }
            ),
            'location': forms.Textarea(
                attrs={
                    'placeholder': "Location"
                }
            ),
        }


class EditGuildForm(BaseGuildForm):
    class Meta(BaseGuildForm.Meta):
        labels = {
            'guild_name': "",
            'guild_description': "",
            'location': "",
            'guild_picture': "Guild Photo",
        }

        widgets ={
            'guild_name': forms.TextInput(
                attrs={
                    'placeholder': "Guild name"
                }
            ),
            'guild_description': forms.Textarea(
                attrs={
                    'placeholder': "Guild description"
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'placeholder': "Location"
                }
            ),
            'guild_picture': forms.FileInput(),
        }