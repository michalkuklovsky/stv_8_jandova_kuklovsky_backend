from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from bokksapp.models import Authors, Books, Genres
from bokksapp.serializers.books_serializer import PostBookSerializer
from bokksapp.views.events import handle_uploaded_file

booksGetColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'quantity', 'authors', 'authors__name', 'genres__id', 'genres__name']


def get_books(request):
    parameters = dict()
    parameters['page'] = request.GET.get('page', 1)
    parameters['per_page'] = request.GET.get('per_page', 20)

    if 'user' in request.session and request.session['user']['is_admin']:
        books = Books.objects.values(*booksGetColumns).distinct('id')
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
    post_data = request.data

    if 'image' in request.FILES:
        file = request.FILES['image']
    else:
        file = None

    errors, book_data = check_req(post_data, file)
    if errors:
        return errors, 422

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

    # Find genre
    genre_names = post_data['genres'].split(', ')
    genres = list()
    for genre_name in genre_names:
        genre = Genres.objects.filter(name__iexact=genre_name).values_list('id', flat=True).first()
        if genre is not None:
            genres.append(genre)
        else:
            return {'errors': {'genre': f'"{genre_name}" does not exist'}}, 400

    book_data['authors'] = list(authors)
    book_data['genres'] = list(genres)

    # book_data['authors'] = authors[0]
    # book_data['genres'] = genres[0]
    if file:
        del book_data['image']
    book = PostBookSerializer(data=book_data)

    if book.is_valid():
        book.save()
        if file:
            handle_uploaded_file(file, book_data['img_path'], 'books')
        return book.data, 201
    return {'errors': book.errors}, 422


def check_req(req_data, file):
    errors = list()
    book_data = {}
    for param in req_data:
        if req_data[param] == "" or req_data[param] == " ":
            errors.append({f'{param}': 'Empty string not allowed'})
        if param == "quantity" or param == "price":
            book_data[param] = float(req_data[param])
        elif param == "release_year":
            book_data[param] = int(req_data[param])

        else:
            book_data[param] = req_data[param]

    if 'img_path' in req_data and file is None:
        errors.append({'field': 'image', 'reasons': 'img_path provided but file is missing'})

    if file is not None and 'img_path' not in req_data:
        errors.append({'field': 'img_path', 'reasons': 'image provided but img_path is missing'})
    return errors, book_data


@api_view(['GET', 'POST'])
def process_request(request):
    if 'user' in request.session:
        if request.session['user']['is_admin']:
            if request.method == 'GET':
                response, http_status = get_books(request)
            elif request.method == 'POST':
                response, http_status = post_book(request)
        else:
            response = {'errors': {'message': 'Unauthorized'}}
            http_status = 401
    else:
        response = {'errors': {'message': 'Forbidden'}}
        http_status = 403

    return JsonResponse(response, status=http_status, safe=False)

