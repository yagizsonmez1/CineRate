from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from movies.models import Review, Favorite

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movies:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request):
    user_reviews = (
        Review.objects
        .filter(user=request.user)
        .select_related("movie")
        .order_by("-created_at")
    )

    fav_qs = Favorite.objects.filter(user=request.user).select_related("movie")
    favorites = [f.movie for f in fav_qs]

    return render(
        request,
        "accounts/profile.html",
        {"favorites": favorites, "user_reviews": user_reviews},
    )
