import os
from datetime import date
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CineRate_project.settings')

import django
django.setup()

from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.contrib.auth.models import User
from movies.models import Movie, Review, Favorite

POSTERS_DIR = Path(settings.MEDIA_ROOT) / "posters"

def add_poster(instance, poster_filename):
    if not poster_filename:
        return
    poster_path = POSTERS_DIR / poster_filename
    if poster_path.exists():
        if instance.poster:
            instance.poster.delete(save=False)
        with open(poster_path, "rb") as f:
            instance.poster.save(poster_filename, File(f), save=True)

@transaction.atomic
def populate():
    user1, _ = User.objects.get_or_create(username="alice")
    user1.set_password("testpass123"); user1.save()
    user2, _ = User.objects.get_or_create(username="bob")
    user2.set_password("testpass123"); user2.save()

    movie1, _ = Movie.objects.get_or_create(
        title="Coach Carter",
        defaults={
            "genre": "Drama",
            "description": "A basketball coach benches his team for bad academic results.",
            "release_date": date(2005, 1, 14),
        },
    )
    add_poster(movie1, "coach_carter.jpg")

    movie2, _ = Movie.objects.get_or_create(
        title="Life is Beautiful",
        defaults={
            "genre": "Drama/Romance",
            "description": "A man uses humor to protect his family during the Holocaust.",
            "release_date": date(1997, 12, 20),
        },
    )
    add_poster(movie2, "life_is_beautiful.jpg")

    movie3, _ = Movie.objects.get_or_create(
        title="Avengers: Infinity War",
        defaults={
            "genre": "Action/Sci-Fi",
            "description": "The Avengers face Thanos in a battle for the Infinity Stones.",
            "release_date": date(2018, 4, 27),
        },
    )
    add_poster(movie3, "infinity_war.jpg")

    Review.objects.get_or_create(movie=movie1, user=user1, defaults={"rating": 5, "text": "Mind-blowing!"})
    Review.objects.get_or_create(movie=movie2, user=user2, defaults={"rating": 4, "text": "Amazing movie!"})
    Review.objects.get_or_create(movie=movie3, user=user1, defaults={"rating": 5, "text": "Masterpiece!"})
    Review.objects.get_or_create(movie=movie1, user=user2, defaults={"rating": 4, "text": "Inspiring story!"})
    Review.objects.get_or_create(movie=movie2, user=user1, defaults={"rating": 5, "text": "Heartwarming and emotional."})
    Review.objects.get_or_create(movie=movie3, user=user2, defaults={"rating": 5, "text": "Epic and thrilling!"})

    Favorite.objects.get_or_create(user=user1, movie=movie2)
    Favorite.objects.get_or_create(user=user2, movie=movie1)
    Favorite.objects.get_or_create(user=user1, movie=movie3)

    from movies.models import Movie as M, Review as R, Favorite as F
    print(f"Done. Movies={M.objects.count()}, Reviews={R.objects.count()}, Favorites={F.objects.count()}")

if __name__ == "__main__":
    populate()
