from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import PositiveSmallIntegerField
from django.contrib.auth.models import  AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


STATUS_CHOICES = (
    ('pro', 'Pro'),
    ('simple', 'Simple'),
)

class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                           validators=[MinValueValidator(18)])

    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

class Country(models.Model):
   country_name = models.CharField(max_length=32, unique=True)

   def str(self):
       return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=32)
    biography = models.TextField()
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    director_image = models.ImageField(upload_to='director_images/', null=True, blank=True)

    def str(self):
        return f'{self.director_name}-{self.biography}-{self.age}'


class Actor(models.Model):
    actor_name = models.CharField(max_length=25)
    biography = models.TextField()
    age = PositiveSmallIntegerField(default=0, null=True, blank=True)
    actor_image = models.ImageField(upload_to='actor_images/', null=True, blank=True)

    def str(self):
        return self.actor_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=20, unique=True)

    def str(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=32)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='movie_country')
    director = models.ManyToManyField(Director, related_name='director_movie')
    actor = models.ManyToManyField(Actor, related_name='actor_movie')
    genre = models.ManyToManyField(Genre, related_name='genre_movie')
    TYPES_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    )
    types = MultiSelectField(choices=TYPES_CHOICES, max_choices=5, max_length=5)
    movie_time = models.PositiveIntegerField()
    description = models.TextField()
    movie_trailer = models.FileField(upload_to='movie_trailer/', null=True, blank=True)
    movie_image = models.ImageField(upload_to='movie_image/', null=True, blank=True)
    status_movie = models.CharField(max_length=32, choices=STATUS_CHOICES, default='simple')

    def str(self):
        return self.movie_name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(ratings.stars for ratings in ratings) / ratings.count(), 1)
        return 0


class MovieLanguages(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='vid/', verbose_name='видео', null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def str(self):
        return self.language


class Moments(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  movie_moments = models.ImageField(upload_to='movie_moments/', null=True, blank=True)

  def str(self):
      return f'{self.movie}'

class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,11)], verbose_name="Рейтинг")
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_date =models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user}-{self.stars}-{self.movie}'

class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user.username}'

class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def str(self):
        return f'{self.movie}-{self.cart}'

class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.movie}-{self.user}'