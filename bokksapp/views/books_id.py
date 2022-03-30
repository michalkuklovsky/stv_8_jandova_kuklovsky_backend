from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from bokksapp.models import Books
from datetime import datetime
from bokksapp.views.books import check_req
from bokksapp.serializers.books_serializer import PutBookSerializer
from bokksapp.views.events import handle_uploaded_file


bookGetColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'quantity', 'authors__id', 'authors__name', 'genres__id', 'genres__name']


def get_book(request, id):
    if 'user' in request.session and request.session['user']['is_admin']:
        book = Books.objects.values(*bookGetColumns).filter(pk=id).first()
    else:
        book = Books.objects.values(*bookGetColumns).filter(pk=id, deleted_at__isnull=True).first()

    if book is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    response = {'book': book}
    return response, 200


def put_book(request, id):
    try:
        Books.objects.get(pk=id)
    except Books.DoesNotExist:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    put_data = request.data

    if 'image' in request.FILES:
        file = request.FILES['image']
    else:
        file = None

    errors, book_data = check_req(put_data, file)
    if errors:
        return errors, 422

    if 'deleted_at' in book_data:
        if book_data['deleted_at'] == 'recover':
            book_data['deleted_at'] = None
        if book_data['deleted_at'] == 'delete':
            book_data['deleted_at'] = datetime.now()

    if file:
        del book_data['image']
        handle_uploaded_file(file, book_data['img_path'], 'books')

    Books.objects.filter(id=id).update(**book_data)

    book = Books.objects.get(pk=id)
    response = {'book': PutBookSerializer(book).data}
    return response, 200


def delete_book(id):
    try:
        book = Books.objects.get(pk=id)
    except Books.DoesNotExist:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404
    book.updated_at = datetime.now()
    book.deleted_at = datetime.now()
    book.save()
    return HttpResponse(status=204)


@api_view(['GET', 'DELETE', 'PUT'])
def process_request(request, id):
    if request.method == 'GET':
        response, http_status = get_book(request, id)

    elif request.method == 'PUT':
        if 'user' in request.session:
            if request.session['user']['is_admin']:
                response, http_status = put_book(request, id)
            else:
                response = {'errors': {'message': 'Unauthorized'}}
                http_status = 401
        else:
            response = {'errors': {'message': 'Forbidden'}}
            http_status = 403

    elif request.method == 'DELETE':
        if 'user' in request.session:
            if request.session['user']['is_admin']:
                return delete_book(id)
            else:
                response = {'errors': {'message': 'Unauthorized'}}
                http_status = 401
        else:
            response = {'errors': {'message': 'Forbidden'}}
            http_status = 403

    return JsonResponse(response, status=http_status, safe=False)
