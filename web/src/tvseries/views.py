from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render

from .models import Imdb, Tvdb, MyRatings

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def imdb_index(request):
    # Parameters.
    title = '' if request.GET.get('title') is None else request.GET.get('title')
    selected_genres = [x.lower() for x in request.GET.getlist('genres')]
    sort_by = 'prediction_desc' if request.GET.get('sort_by') is None else request.GET.get('sort_by')
    page_number = 1 if request.GET.get('page') is None else request.GET.get('page')

    # Get databases.
    imdb_list = Imdb.objects.all()
    tvdb_list = Tvdb.objects.all()
    my_ratings_list = MyRatings.objects.all().values()

    # Filter genres.
    if len(selected_genres) > 0:
        for genre in selected_genres:
            argument = {f'genre_{genre}__contains': '1'}
            imdb_list = imdb_list.filter(**argument)
    imdb_list = imdb_list.values()

    # Filter titles.
    tvdb_list = tvdb_list \
        .filter(imdb_id__in=[item.get('id') for item in imdb_list],
                series_name__icontains=title)

    # Sort titles.
    argument = sort_by.split("_")[0]

    if argument == 'prediction':
        if 'asc' in sort_by:
            tvdb_list = tvdb_list \
                .order_by(F('prediction').asc(nulls_last=True), 'imdb_id') \
                .values()
        else:
            tvdb_list = tvdb_list \
                .order_by(F('prediction').desc(nulls_last=True), 'imdb_id') \
                .values()
    else:
        tvdb_list = tvdb_list.filter(prediction__exact=None).values()
        for i, item in enumerate(tvdb_list):
            tvdb_list[i]['my_rating'] = next((x['my_rating'] for x in my_ratings_list if item["imdb_id"] == x['imdb_id']), None)
        tvdb_list = list(filter(lambda x: x['my_rating'] is not None, tvdb_list))
        tvdb_list = sorted(tvdb_list, key=lambda x: x['my_rating'], reverse='asc' not in sort_by)

    paginator = Paginator(tvdb_list, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'imdb': imdb_list,
        'tvdb': page_obj,
        'my_ratings': my_ratings_list,
        'selected_genres': selected_genres,
        'sort_by': sort_by,
        'last_page': paginator.num_pages
    }

    return render(request, 'templates/imdb_index.html', context)


def imdb_detail(request, imdb_id):
    imdb = Imdb.objects.get(id=imdb_id)
    tvdb = Tvdb.objects.get(imdb_id=imdb_id)

    context = {
        'imdb': imdb,
        'tvdb': tvdb,
    }
    return render(request, 'templates/imdb_detail.html', context)
