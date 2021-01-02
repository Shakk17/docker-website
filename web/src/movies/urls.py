from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path("", views.movies_index, name="movies_index"),
    path("<str:imdb_id>/", views.movies_detail, name="movies_detail"),
]
