from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.register, name='login' ),
    path('movies/', views.movie_list, name='movie_list'), 
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
]