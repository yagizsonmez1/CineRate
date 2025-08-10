from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Favorite, Movie, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ReviewForm
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator # This handles splitting  the movie list into pages
from django.db.models import Q # lets us filter

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
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = movie.favorite_set.filter(user=request.user).exists()
         
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'existing_review': existing_review,
        'is_favorite': is_favorite,
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
    user_profile = get_object_or_404(User, pk=user_id)
    favorites = Favorite.objects.filter(user=user_profile).select_related('movie')
    reviews = Review.objects.filter(user=user_profile).select_related('movie')

    context = {
        'user_profile' : user_profile,
        'favorites' : favorites,
        "reviews" : reviews,
    }
    return render(request, "movies/profile.html", context
                  )
@login_required
def toggle_favorite(request, movie_id):
    movie = movie = get_object_or_404(Movie, pk=movie_id)
    favorite = Favorite.objects.filter(user=request.user, movie=movie).first()

    if favorite:
        favorite.delete()
        is_favorite = False
    else:
        Favorite.objects.create(user=request.user, movie=movie)
        is_favorite = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite' : is_favorite })

    return redirect('movies:movie_detail', movie_id=movie.id)

def movie_list(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(genre__icontains=query)|
            Q(description__icontains=query)
        )
    
    paginator = Paginator(movies, 6) # 6 movies per page is enough I think
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'movies/movie_list.html', {
        'page_obj': page_obj,
        'query': query
    })