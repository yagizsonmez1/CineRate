from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ReviewForm
from django.http import HttpResponseForbidden

def register(request):
    return HttpResponse("Register page coming soon.") # Just to avoid the breakdown of the site

def login(request):
    return HttpResponse("Login page coming soon") # Just to avoid the breakdown of the site


def home(request):
    return render(request, "movies/home.html")

def movie_list(request):
    movies = Movie.objects.all()
    return render (request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')

    existing_review = None # Checking if the user has already submitted a review
    if request.user.is_authenticated:
        existing_review = Review.objects.filter(movie=movie, user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movies:movie_detail', movie_id=movie.id)
    if request.user.is_authenticated:
        form = ReviewForm(instance=existing_review)
    else:
        None 
        
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'existing_review': existing_review,
    })

@login_required
def delete_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review = get_object_or_404(Review, movie=movie, user=request.user)

    if request.method == 'POST':
        review.delete()
        return redirect('movies:movie.detail', movie_id=movie.id)
    return HttpResponseForbidden("You can't do that.")

@login_required
def profile(request, user_id):
    return render(request, 'movies/profile.html', {'user_id':user_id})


