from django import template

register = template.Library()


@register.filter
def get_rating_by_imdb_id(my_ratings_list, imdb_id):
    item = next((item for item in my_ratings_list if item["imdb_id"] == imdb_id), None)
    return item['my_rating']


@register.filter
def get_n_pages(array):
    return int(len(array) / 20)


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
        genres = sorted(genres)
        if len(genres) > 3:
            genres = genres[:3] + [f'+{len(genres)-3}']
    except AttributeError:
        genres = []
    return genres
