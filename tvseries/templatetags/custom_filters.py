from django.template.defaulttags import register


@register.filter
def get_prediction_by_imdb_id(tvdb_list, imdb_id):
    return next((item['prediction'] for item in tvdb_list if item["imdb_id"] == imdb_id), None)


@register.filter
def get_rating_by_imdb_id(my_ratings_list, imdb_id):
    return next((item['my_rating'] for item in my_ratings_list if item["imdb_id"] == imdb_id), None)


@register.filter
def get_n_pages(array):
    return int(len(array) / 10)


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def get_all_genres(imdb):
    genres = ['-'.join(name.split('_')[1:]).capitalize()
              for (name, value) in imdb[0].items()
              if name.startswith('genre')]
    return sorted(genres)


@register.filter
def get_genres(item):
    """Returns a list containing all the genres of an IMDb series."""
    vars_dict = vars(item)
    genres = ['-'.join(name.split('_')[1:]).capitalize()
              for (name, value) in vars_dict.items()
              if name.startswith('genre') and value == 1]
    return sorted(genres)


@register.filter
def get_genres_by_imdb_id(imdb_list, imdb_id):
    item = next((item for item in imdb_list if item["id"] == imdb_id), None)
    try:
        genres = ['-'.join(name.split('_')[1:]).capitalize()
                  for (name, value) in item.items()
                  if name.startswith('genre') and value == 1]
    except AttributeError:
        genres = []
    return sorted(genres)
