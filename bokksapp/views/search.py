import json

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, F, Max
from rest_framework.decorators import api_view


from bokksapp.models import Books
from bokksapp.models import Authors
from bokksapp.models import Genres

booksColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'authors__id', 'authors__name', 'genres__id', 'genres__name']

# default values
PAGE = 1
PER_PAGE = 20
ORDER_BY = 'id'
ORDER_TYPE = 'asc'

# GET /search endpoint
def searchEvents(request):
    query_parameters = parse_request(request)  # gets paramaters from request
    query_parameters = check_and_set_parameters(query_parameters)  # checks parameters and set defaults if needed

    # creates query from parameteres
    try:
        page, paginator = get_query(query_parameters)
    except:
        response = {'errors': {'message': 'Both filter and filter_by must be provided to filter results'}}
        return response, 422
    response = serialize_object(query_parameters, page, paginator)

    return response, 200

# copy parameters from QueryDict to Dict
def parse_request(request):
    r = request.GET
    return {
        'page': r.get('page'),
        'per_page': PER_PAGE,
        'order_by': r.get('order_by'),
        'order_type': r.get('order_type'),
        'filter_by': r.get('filter_by'),
        'filter': r.get('filter'),
        'query': r.get('query')
    }


# control function for GET request; if parameters are wrong, default settings are used
def check_and_set_parameters(query_parameters):
    if not query_parameters['page']:
        query_parameters['page'] = PAGE
    try:
        if int(query_parameters['page']) < PAGE:
            query_parameters['page'] = PAGE
    except ValueError:
        query_parameters['page'] = 1

    if not query_parameters['order_by'] or str(query_parameters['order_by']).lower() not in ['price', 'release_year']:
        query_parameters['order_by'] = ORDER_BY

    if not query_parameters['order_type'] or str(query_parameters['order_type']).lower() != 'desc':
        query_parameters['order_type'] = ORDER_TYPE

    if not query_parameters['filter_by'] or str(query_parameters['filter_by']).lower() not in ['author', 'genre']:
        query_parameters['filter_by'] = None

    return query_parameters

def get_query(query_parameters):
    books = Books.objects.values(*booksColumns).filter(deleted_at__isnull=True).all()

    if query_parameters['query'] is not None:                                                   # query
        books = books.filter(
            Q(authors__name__icontains=query_parameters['query']) |
            Q(title__icontains=query_parameters['query']) |
            Q(description__icontains=query_parameters['query'])
        )

    if query_parameters['filter'] is not None and query_parameters['filter_by'] is not None:  
        if query_parameters['filter_by'] == 'author':
            books = books.filter(Q(authors__name__icontains=query_parameters['filter']))
        else:
            books = books.filter(Q(genres__name__icontains=query_parameters['filter']))
    else:
        if query_parameters['filter'] is not None or query_parameters['filter_by'] is not None:
            raise ValueError("Missing: Both filter and filter_by must be provided!")

    if query_parameters['order_type'] == 'asc':                                                # order_by, order_type
        response = books.order_by(F(query_parameters['order_by']).asc(nulls_last=True))
    else:
        response = books.order_by(F(query_parameters['order_by']).desc(nulls_last=True))

    paginator = Paginator(response, query_parameters['per_page'])

    if paginator.num_pages >= int(query_parameters['page']):
        page = paginator.get_page(query_parameters['page'])
    else:
        page = []

    return page, paginator

# creates response for GET /search request
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

@api_view(['GET'])
def processRequest(request):
    if request.method == 'GET':
        response, http_status = searchEvents(request)
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)