# import imp
# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from bokksapp.models import Books
# from bokksapp.models import Authors
# from bokksapp.models import BooksHasAuthors


def homepage(request):
	html = "<html>" \
			"<body>" \
			"Homepage" \
			"</body>" \
			"</html>"
	return HttpResponse(html)

