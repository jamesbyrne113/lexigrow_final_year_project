from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import LexiGrowUserCreationForm, LexiGrowUserChangeForm
from .models import LexiGrowUser

class LexiGrowUserAdmin(UserAdmin):
    add_form = LexiGrowUserCreationForm
    form = LexiGrowUserChangeForm
    model = LexiGrowUser
    list_display = ['email', 'first_name', 'last_name', 'level', "show_harder_words"]

admin.site.register(LexiGrowUser, LexiGrowUserAdmin)
