from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework.decorators import api_view
from bokksapp.models import Books, Genres

booksColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'authors__id', 'authors__name', 'genres__id', 'genres__name']


def get_genres():
    parameters = dict()
    parameters['page'] = 1
    parameters['per_page'] = 8

    genres = Genres.objects.values('id', 'name')

    paginator = Paginator(genres, parameters['per_page'])
    if paginator.num_pages >= int(parameters['page']):
        page = paginator.get_page(parameters['page'])
    else:
        page = []

    response = serialize_object(parameters, page, paginator, 'genres')

    return response, 200


def select_books(request, genre):
    parameters = dict()
    parameters['page'] = request.GET.get('page', 1)
    parameters['per_page'] = request.GET.get('per_page', 8)

    books = Books.objects.values(*booksColumns).all().filter(genres__name__icontains=genre)

    paginator = Paginator(books, parameters['per_page'])
    if paginator.num_pages >= int(parameters['page']):
        page = paginator.get_page(parameters['page'])
    else:
        page = []

    response = serialize_object(parameters, page, paginator, 'books')

    return response, 200


def serialize_object(parameters, page, paginator, items):
    response = {f'{items}': list(page),
                'metadata': {
                    'page': int(parameters['page']),
                    'per_page': int(parameters['per_page']),
                    'pages': paginator.num_pages,
                    'total': paginator.count,
                    }
                }
    return response


@api_view(['GET'])
def process_request(request):
    if request.method == 'GET':
        genre = request.GET.get('query', None)
        if genre:
            response, http_status = select_books(request, genre)
        else:
            response, http_status = get_genres()
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)

