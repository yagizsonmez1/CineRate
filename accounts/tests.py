from datetime import date
from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User



from movies.models import Movie, Review, Favorite

@override_settings(MEDIA_ROOT="/tmp/django_test_media/")
class CineRateTests(TestCase):
    """
    One-file test suite for both 'accounts' and 'movies' bits.
    Safe to live here; Django will discover it.
    """

    @classmethod
    def setUpTestData(cls):
        # Users
        cls.user = User.objects.create_user(
            username="alice", password="pass123", email="a@example.com"
        )
        cls.other = User.objects.create_user(
            username="bob", password="pass123", email="b@example.com"
        )

        # Movies (7 so we exercise pagination size=6)
        cls.m1 = Movie.objects.create(title="Interstellar", genre="Sci-Fi", description="Space", release_date=date(2014,11,7))
        cls.m2 = Movie.objects.create(title="Inception", genre="Sci-Fi", description="Dreams", release_date=date(2010,7,16))
        cls.m3 = Movie.objects.create(title="Pulp Fiction", genre="Crime", description="Nonlinear", release_date=date(1994,10,14))
        cls.m4 = Movie.objects.create(title="The Prestige", genre="Drama", description="Magicians", release_date=date(2006,10,20))
        cls.m5 = Movie.objects.create(title="Shutter Island", genre="Thriller", description="Island", release_date=date(2010,2,19))
        cls.m6 = Movie.objects.create(title="La La Land", genre="Musical", description="LA", release_date=date(2016,12,9))
        cls.m7 = Movie.objects.create(title="The Matrix", genre="Sci-Fi", description="Simulation", release_date=date(1999,3,31))

        # Existing review owned by alice on m1 (so update/delete can be tested)
        cls.existing = Review.objects.create(user=cls.user, movie=cls.m1, rating=4, text="Great!")

    def setUp(self):
        self.client = Client()

    # ---------- URL sanity ----------
    def test_named_urls_exist(self):
        for name in ["movies:home", "movies:movie_list"]:
            self.assertTrue(resolve(reverse(name)))

    # ---------- Public pages ----------
    def test_home_ok(self):
        res = self.client.get(reverse("movies:home"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "movies/home.html")

    def test_movie_list_ok_and_pagination(self):
        res = self.client.get(reverse("movies:movie_list"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("page_obj", res.context)

        # Page 2 should exist because we have 7 movies & page size is 6
        res2 = self.client.get(reverse("movies:movie_list"), {"page": 2})
        self.assertEqual(res2.status_code, 200)

    def test_movie_list_search(self):
        res = self.client.get(reverse("movies:movie_list"), {"q": "fic"})
        self.assertEqual(res.status_code, 200)
        titles = [m.title for m in res.context["page_obj"].object_list]
        self.assertTrue(any("Pulp Fiction" in t for t in titles))

    def test_movie_detail_ok(self):
        res = self.client.get(reverse("movies:movie_detail", args=[self.m1.id]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.m1.title)
        self.assertIn("reviews", res.context)

    # ---------- Reviews ----------
    def test_review_create_requires_login(self):
        url = reverse("movies:movie_detail", args=[self.m2.id])
        res = self.client.post(url, {"rating": 5, "text": "Amazing"}, follow=True)
        # Not logged in → view should not create a review
        self.assertEqual(Review.objects.filter(movie=self.m2).count(), 0)

    def test_review_create_as_user(self):
        self.client.login(username="alice", password="pass123")
        url = reverse("movies:movie_detail", args=[self.m2.id])
        res = self.client.post(url, {"rating": 5, "text": "Amazing"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            Review.objects.filter(movie=self.m2, user=self.user, rating=5, text__icontains="Amazing").exists()
        )

    def test_review_update_when_exists(self):
        self.client.login(username="alice", password="pass123")
        url = reverse("movies:movie_detail", args=[self.m1.id])
        res = self.client.post(url, {"rating": 3, "text": "Changed"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.existing.refresh_from_db()
        self.assertEqual(self.existing.rating, 3)
        self.assertIn("Changed", self.existing.text)

    def test_review_delete(self):
        self.client.login(username="alice", password="pass123")
        url = reverse("movies:delete_review", args=[self.m1.id])
        res = self.client.post(url, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Review.objects.filter(pk=self.existing.pk).exists())

    # ---------- Favorites ----------
    def test_toggle_favorite_add_and_remove(self):
        self.client.login(username="alice", password="pass123")
        url = reverse("movies:toggle_favorite", args=[self.m3.id])

        # Add
        res = self.client.post(url, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user=self.user, movie=self.m3).exists())

        # Remove
        res = self.client.post(url, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user=self.user, movie=self.m3).exists())

    def test_movie_detail_form_visible_when_logged_in(self):
        # Logged-in users should see a review form on the detail page
        self.client.login(username="alice", password="pass123")
        res = self.client.get(reverse("movies:movie_detail", args=[self.m2.id]))
        self.assertEqual(res.status_code, 200)
        # The view should put a form in context for authenticated users
        self.assertIn("form", res.context)
        # And the rendered page should include a rating input
        self.assertContains(res, 'name="rating"', html=False)


    def test_movie_detail_is_favorite_flag_true_when_favorited(self):
        # If the user has favorited the movie, detail context should flag it
        self.client.login(username="alice", password="pass123")
        Favorite.objects.create(user=self.user, movie=self.m3)
        res = self.client.get(reverse("movies:movie_detail", args=[self.m3.id]))
        self.assertEqual(res.status_code, 200)
        self.assertIn("is_favorite", res.context)
        self.assertTrue(res.context["is_favorite"])
