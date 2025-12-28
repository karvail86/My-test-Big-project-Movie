from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

StatusChoices = (
        ('pro', 'pro'),
        ('simple', 'simple'))


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)], null=True, blank=True)
    user_photo = models.ImageField(upload_to='user=images', null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices, default='simple')
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Category(models.Model):
   category_name = models.CharField(max_length=100, unique=True)


   def __str__(self):
       return self.category_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='genres')

    def __str__(self):
        return f'{self.genre_name}, {self.category}'



class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country_name

class Director(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    director_photo = models.ImageField(upload_to='director_images')
    birth_date = models.DateField()
    bio = models.TextField()


    def __str__(self):
        return self.full_name


class Actor(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    actor_photo = models.ImageField(upload_to='actor_images')
    birth_date = models.DateField()
    bio = models.TextField()

    def __str__(self):
        return self.full_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    # slogan =models.CharField(max_length=100, null=True, blank=True)
    year = models.DateField()
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director, related_name='director_movies')
    genre = models.ManyToManyField(Genre)
    MovieTypeChoices = (
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('1080p Ultra', '1080p Ultra'),)
    movie_type = models.CharField(max_length=20, choices=MovieTypeChoices)
    movie_time = models.PositiveSmallIntegerField()
    actor = models.ManyToManyField(Actor, related_name='actor_movies')
    movie_poster = models.ImageField(upload_to='movie_poster')
    trailer = models.URLField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices, default='simple')

    def __str__(self):
        return self.movie_name

    def get_avg_rating(self):
        all_ratings = self.ratings.all()
        if all_ratings.exists():
            return round(sum([i.stars for i in all_ratings]) / all_ratings.count(), 2)
        return 0

    def get_count_rating(self):
        return self.ratings.count()

class MovieVideo(models.Model):
    video_name = models.CharField(max_length=100)
    video = models.FileField(upload_to='video_video')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return f'{self.video_name}, {self.movie}'



class MovieFrame(models.Model):
    image = models.ImageField(upload_to='movie_frame')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='frames')

    def __str__(self):
        return f'{self.movie}, {self.image}'


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveIntegerField(choices=[(i, str(i))for i in range(1, 11)])
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}, {self.movie}, {self.stars}'

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.comment}'



class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'



class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.movie}'



class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.movie}, {self.created_date}'


class ActorImage(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='actor_images')

    def __str__(self):
        return f'{self.actor}, {self.image}'


class ReviewLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f'{self.user}, {self.review}'
