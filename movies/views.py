from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie, Review

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
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews})


