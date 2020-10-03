from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Imdb, Tvdb, MyRatings


def imdb_index(request):
    title = '' if request.GET.get('title') is None else request.GET.get('title')

    page_number = 1 if request.GET.get('page') is None else request.GET.get('page')

    imdb = Imdb.objects\
        .all()\
        .values()

    tvdb_list = Tvdb.objects\
        .filter(series_name__icontains=title)\
        .order_by('-prediction', 'imdb_id')\
        .values()

    my_ratings_list = MyRatings.objects.all().values()

    paginator = Paginator(tvdb_list, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'imdb': imdb,
        'tvdb': page_obj,
        'my_ratings': my_ratings_list,
    }

    return render(request, 'imdb_index.html', context)


def imdb_detail(request, imdb_id):
    imdb = Imdb.objects.get(id=imdb_id)
    tvdb = Tvdb.objects.get(imdb_id=imdb_id)

    context = {
        'imdb': imdb,
        'tvdb': tvdb,
    }
    return render(request, 'imdb_detail.html', context)



