from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Imdb, Tvdb, MyRatings

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def imdb_index(request):
    title = '' if request.GET.get('title') is None else request.GET.get('title')
    selected_genres = [x.lower() for x in request.GET.getlist('genres')]

    page_number = 1 if request.GET.get('page') is None else request.GET.get('page')

    imdb_list = Imdb.objects.all()

    # Genres filter.
    if len(selected_genres) > 0:
        for genre in selected_genres:
            argument = {f'genre_{genre}__contains': '1'}
            imdb_list = imdb_list.filter(**argument)

    imdb_list = imdb_list.values()

    tvdb_list = Tvdb.objects \
        .filter(imdb_id__in=[item.get('id') for item in imdb_list], series_name__icontains=title) \
        .order_by('-prediction', 'imdb_id') \
        .values()

    my_ratings_list = MyRatings.objects.all().values()

    paginator = Paginator(tvdb_list, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'imdb': imdb_list,
        'tvdb': page_obj,
        'my_ratings': my_ratings_list,
        'selected_genres': selected_genres,
    }
    print(selected_genres)
    return render(request, 'imdb_index.html', context)


def imdb_detail(request, imdb_id):
    imdb = Imdb.objects.get(id=imdb_id)
    tvdb = Tvdb.objects.get(imdb_id=imdb_id)

    context = {
        'imdb': imdb,
        'tvdb': tvdb,
    }
    return render(request, 'imdb_detail.html', context)
