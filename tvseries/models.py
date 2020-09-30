from django.db import models


class Imdb(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    rating_avg = models.DecimalField(max_digits=2, decimal_places=2)
    genre_action = models.BooleanField()
    genre_sci_fi = models.BooleanField(db_column='genre_sci-fi')
    genre_mystery = models.BooleanField()
    genre_fantasy = models.BooleanField()
    genre_documentary = models.BooleanField()
    genre_music = models.BooleanField()
    genre_short = models.BooleanField()
    genre_game_show = models.BooleanField(db_column='genre_game-show')
    genre_comedy = models.BooleanField()
    genre_horror = models.BooleanField()
    genre_reality_tv = models.BooleanField(db_column='genre_reality-tv')
    genre_history = models.BooleanField()
    genre_thriller = models.BooleanField()
    genre_musical = models.BooleanField()
    genre_sport = models.BooleanField()
    genre_family = models.BooleanField()
    genre_crime = models.BooleanField()
    genre_drama = models.BooleanField()
    genre_romance = models.BooleanField()
    genre_western = models.BooleanField()
    genre_war = models.BooleanField()
    genre_biography = models.BooleanField()
    genre_animation = models.BooleanField()
    genre_news = models.BooleanField()
    genre_adventure = models.BooleanField()
    genre_talk_show = models.BooleanField(db_column='genre_talk-show')
    poster = models.URLField()

    class Meta:
        db_table = "imdb"
        managed = False


class Tvdb(models.Model):
    imdb_id = models.CharField(max_length=20, primary_key=True)
    series_name = models.CharField(max_length=200)
    overview = models.TextField()
    prediction = models.DecimalField(max_digits=2, decimal_places=2)

    class Meta:
        db_table = "tvdb"
        managed = False
        ordering = ['-prediction']


class MyRatings(models.Model):
    imdb_id = models.CharField(max_length=20, primary_key=True)
    my_rating = models.IntegerField()

    class Meta:
        db_table = 'my_ratings'
        managed = False