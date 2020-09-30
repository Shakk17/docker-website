from django.template.defaulttags import register


@register.filter
def get_prediction_by_id(array, imdb_id):
    return next((item['prediction'] for item in array if item["imdb_id"] == imdb_id), None)


@register.filter
def get_poster_by_id(array, imdb_id):
    return next((item['poster'] for item in array if item["imdb_id"] == imdb_id), None)


@register.filter
def get_n_pages(array):
    return int(len(array) / 10)


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()


@register.filter
def get_genres(item):
    vars_dict = vars(item)
    genres = ['-'.join(name.split('_')[1:]).capitalize() for (name, value) in vars_dict.items() if name.startswith('genre') and value == 1]
    return genres
