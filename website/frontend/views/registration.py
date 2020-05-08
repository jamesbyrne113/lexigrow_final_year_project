from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from frontend.forms import LexiGrowUserOptionsChange, LexiGrowUserCreationForm
from frontend.models import LexiGrowUser


def signup(request):
    if request.method == 'POST':
        form = LexiGrowUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = LexiGrowUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def update_user_options(request):
    user = LexiGrowUser.objects.get(email=request.user.email)

    if request.method == 'POST':
        form = LexiGrowUserOptionsChange(request.POST)

        if form.is_valid():
            user.level = request.POST["level"]
            user.show_harder_words = True if request.POST.get("show_harder_words", None) == "on" else False
            user.save()

            return redirect('/')
    else:
        form = LexiGrowUserOptionsChange(initial={'level': user.level, 'show_harder_words': user.show_harder_words})
    return render(request, 'registration/change.html', {'form': form})