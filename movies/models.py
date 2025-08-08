from django.db import models
from django.conf import settings

class Movie(models.Model): #I created it since I am working on the html templates I needed it.
    title = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    release_date = models.DateField()
 
    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        unique_together = ('movie', 'user')

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
 
    class Meta:
        unique_together = ('user', 'movie')