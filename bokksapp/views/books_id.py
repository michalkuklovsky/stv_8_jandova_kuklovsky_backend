from django.http import JsonResponse

# from rest_framework.decorators import api_view
from bokksapp.models import Books

bookGetColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'authors__id', 'authors__name', 'genres__id', 'genres__name']


def get_book(id):
    book = Books.objects.values(*bookGetColumns).filter(id=id).first()

    if book is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    response = {'book': book}
    return response, 200


def put_book(id):
    book = Books.objects.values(*bookGetColumns).filter(id=id).first()

    if book is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    response = {'book': book}
    return response, 200


def check_body(request):
    req_params = []


def delete_book(id):
    try:
        Books.objects.filter(id=id).delete()
    except:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    return [], 204


# @api_view(['GET', 'DELETE', 'PUT'])
def process_request(request, id):
    if request.method == 'GET':
        response, http_status = get_book(id)
    elif request.method == 'PUT':
        response, http_status = put_book(id)
    elif request.method == 'DELETE':
        response, http_status = delete_book(id)
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)
