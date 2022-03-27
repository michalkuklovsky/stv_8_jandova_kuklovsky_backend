from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from bokksapp.models import Books
from datetime import datetime
from django.db.models import Q
from bokksapp.serializers.books_serializer import GetBooksSerializer

bookGetColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'quantity', 'authors__id', 'authors__name', 'genres__id', 'genres__name']


def get_book(id):
    # if user == 'admin':
    #   book = Books.objects.values(*bookGetColumns).filter(pk=id)).first()
    # else:
    book = Books.objects.values(*bookGetColumns).filter(pk=id, deleted_at__isnull=True).first()

    if book is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    # book = Books.objects.get(pk=id)
    # book = GetBooksSerializer(book).data
    response = {'book': book}
    return response, 200


def put_book(request, id):
    put_data = JSONParser().parse(request)
    check_req(put_data)
    try:
        book = Books.objects.get(pk=id)
    except Books.DoesNotExist:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    response = {'book': book}
    return response, 200


def check_req(put_data):
    pass


def delete_book(id):
    try:
        book = Books.objects.get(pk=id)
    except Books.DoesNotExist:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404
    book.updated_at = datetime.now()
    book.deleted_at = datetime.now()
    book.save()
    return None, 204


@api_view(['GET', 'DELETE', 'PUT'])
def process_request(request, id):
    if request.method == 'GET':
        response, http_status = get_book(id)
    elif request.method == 'PUT':
        response, http_status = put_book(request, id)
    elif request.method == 'DELETE':
        response, http_status = delete_book(id)
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)
