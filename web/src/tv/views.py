from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Imdb, MyRatings


@csrf_exempt
def imdb_index(request):
    # Parameters.
    title = '' if request.GET.get('title') is None else request.GET.get('title')
    selected_genres = [x.lower() for x in request.GET.getlist('genres')]
    sort_by = 'prediction_desc' if request.GET.get('sort_by') is None else request.GET.get('sort_by')
    page_number = 1 if request.GET.get('page') is None else request.GET.get('page')

    # Get databases.
    imdb_list = Imdb.objects.all()
    my_ratings_list = MyRatings.objects.all().values()

    # Filter genres.
    if len(selected_genres) > 0:
        for genre in selected_genres:
            argument = {f'genre_{genre}__contains': '1'}
            imdb_list = imdb_list.filter(**argument)

    # Filter titles.
    imdb_list = imdb_list \
        .filter(name__icontains=title)

    # Sort titles by prediction value.
    if sort_by.split("_")[0] == 'prediction':
        if 'asc' in sort_by:
            imdb_list = imdb_list \
                .order_by(F('prediction').asc(nulls_last=True), 'id') \
                .values()
        else:
            imdb_list = imdb_list \
                .order_by(F('prediction').desc(nulls_last=True), 'id') \
                .values()
    # Sort titles by rating value.
    else:
        # Get all the shows already watched.
        imdb_list = imdb_list.filter(prediction__exact=None).values()
        for i, item in enumerate(imdb_list):
            imdb_list[i]['my_rating'] = next((x['my_rating'] for x in my_ratings_list if item["id"] == x['imdb_id']), None)
        imdb_list = list(filter(lambda x: x['my_rating'] is not None, imdb_list))
        imdb_list = sorted(imdb_list, key=lambda x: x['my_rating'], reverse='asc' not in sort_by)

    paginator = Paginator(imdb_list, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'imdb': page_obj,
        'my_ratings': my_ratings_list,
        'selected_genres': selected_genres,
        'sort_by': sort_by,
        'last_page': paginator.num_pages
    }

    return render(request, 'imdb_index.html', context)


def imdb_detail(request, imdb_id):
    imdb = Imdb.objects.get(id=imdb_id)

    context = {
        'imdb': imdb
    }
    return render(request, 'imdb_detail.html', context)
