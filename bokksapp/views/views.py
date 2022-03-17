import imp
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from bokksapp.models import Books
from bokksapp.models import Authors
from bokksapp.models import BooksHasAuthors

booksColumns = ['id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path']
authorColumns = ['id', 'name']
booksHasAuthorsColumns = ['book_id', 'author_id']

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
	return JsonResponse(response, status=http_status)

# creates response for GET request
def serialize_object(str, get):
    return {str: get}

# GET endpoint
def get_id(request, id):
    book = Books.objects.values(*booksColumns).filter(id=id).first()
    if book is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    key = BooksHasAuthors.objects.values(*booksHasAuthorsColumns).filter(author=id).first()
    if key is None:
        return {'error': {'message': 'Internal server error'}}, 501
    author_id = key['author_id']

    author = Authors.objects.values(*authorColumns).filter(id=author_id).first()
    if author is None:
        return {'error': {'message': 'Internal server error'}}, 501

    book['author_id'] = author['id']
    book['author'] = author['name']

    response = serialize_object('book', book)
    return response, 200
