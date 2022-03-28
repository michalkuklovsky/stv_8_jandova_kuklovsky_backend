from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from bokksapp.models import Authors, Books, Genres
from bokksapp.serializers.books_serializer import AuthorSerializer,GenreSerializer, GetBooksSerializer, PostBookSerializer

booksGetColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'authors__id', 'authors__name', 'genres__id', 'genres__name']


def get_books(request):
    parameters = dict()
    parameters['page'] = request.GET.get('page', 1)
    parameters['per_page'] = request.GET.get('per_page', 20)

    if request.session['user']['is_admin']:
        books = Books.objects.values(*booksGetColumns)
    else:
        books = Books.objects.values(*booksGetColumns).filter(deleted_at__isnull=True).distinct('id')

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


def post_book(request):
    post_data = JSONParser().parse(request)

    # Find author
    author_names = post_data['authors'].split(', ')
    authors = list()
    for author_name in author_names:
        author = Authors.objects.filter(name__iexact=author_name).values_list('id', flat=True).first()

        if author is not None:
            authors.append(author)
        else:
            author = Authors.objects.create(name=author_name)
            authors.append(author.id)
            # return {'errors': {'author': 'Does not exist'}}, 400

    # Find genre
    genre_names = post_data['genres'].split(', ')
    genres = list()
    for genre_name in genre_names:
        genre = Genres.objects.filter(name__iexact=genre_name).values_list('id', flat=True).first()
        if genre is not None:
            genres.append(genre)
        else:
            return {'errors': {'genre': f'"{genre_name}" does not exist'}}, 400

    post_data['authors'] = list(authors)
    post_data['genres'] = list(genres)

    book = PostBookSerializer(data=post_data)

    if book.is_valid():
        book.save()
        return book.data, 200
    return {'errors': book.errors}, 400


@api_view(['GET', 'POST'])
def process_request(request):
    if request.method == 'GET':
        response, http_status = get_books(request)
    elif request.method == 'POST' and request.session['user']['is_admin']:
        response, http_status = post_book(request)
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)

