from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/delete_review/', views.delete_review, name='delete_review'),
    path('movies/<int:movie_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
]
