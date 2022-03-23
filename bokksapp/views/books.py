from django.http import JsonResponse
from django.core.paginator import Paginator

# from rest_framework.decorators import api_view
from bokksapp.models import Books

booksGetColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'authors__id', 'authors__name', 'genres__id', 'genres__name']


def get_books(request):
    parameters = dict()
    parameters['page'] = request.GET.get('page', 1)
    parameters['per_page'] = request.GET.get('per_page', 8)

    books = Books.objects.values(*booksGetColumns)

    paginator = Paginator(books, parameters['per_page'])
    if paginator.num_pages >= int(parameters['page']):
        page = paginator.get_page(parameters['page'])
    else:
        page = []

    response = serialize_object(parameters, page, paginator)

    return response, 200


def serialize_object(parameters, page, paginator):
    response = {'books': list(page),
                'metadata': {
                    'page': int(parameters['page']),
                    'per_page': int(parameters['per_page']),
                    'pages': paginator.num_pages,
                    'total': paginator.count,
                    }
                }
    return response

# @api_view(['GET', 'POST'])
def process_request(request):
    if request.method == 'GET':
        response, http_status = get_books(request)
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)

