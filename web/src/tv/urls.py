from django.urls import path

from . import views

app_name = 'tv'
urlpatterns = [
    path("", views.imdb_index, name="imdb_index"),
    path("<str:imdb_id>/", views.imdb_detail, name="imdb_detail"),
]
