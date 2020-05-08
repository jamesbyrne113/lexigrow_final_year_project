from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import LexiGrowUser

class LexiGrowUserCreationForm(UserCreationForm):

    class Meta:
        model = LexiGrowUser
        fields = ('email', 'first_name', 'last_name', 'level',)


class LexiGrowUserChangeForm(UserChangeForm):

    class Meta:
        model = LexiGrowUser
        fields = ('email', 'first_name', 'last_name', 'level',)

class LexiGrowUserOptionsChange(forms.ModelForm):

    class Meta:
        model = LexiGrowUser
        fields = ('level', 'show_harder_words')