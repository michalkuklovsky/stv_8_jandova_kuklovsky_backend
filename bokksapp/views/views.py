# import imp
# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from bokksapp.models import Books
# from bokksapp.models import Authors
# from bokksapp.models import BooksHasAuthors

booksColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'authors__id', 'authors__name', 'genres__id', 'genres__name']

def homepage(request):
	html = "<html>" \
			"<body>" \
			"Homepage" \
			"</body>" \
			"</html>"
	return HttpResponse(html)

def bookIDShowcase(request, id):
	if request.method == 'GET':
		response, http_status = get_id(request, id)
	else:
		response = {'message': 'Bad request'}
		http_status = 400
	return JsonResponse(response, status=http_status, safe=False)

# creates response for GET request
def serialize_object(str, get):
    return {str: get}

# GET endpoint
def get_id(request, id):
    book = Books.objects.values(*booksColumns).filter(id=id).first()

    if book is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    response = serialize_object('book', book)
    return response, 200
