from django.http import HttpResponse, JsonResponse
from rest_framework import status

from bokksapp.models import Books, Events


def homepage(request):
	if request.method == 'GET':
		books = Books.objects.values().all()[:8]
		events = Events.objects.values().all()[:4]
		return JsonResponse({'books': list(books), 'events': list(events)}, status=status.HTTP_200_OK, safe=False)
	return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

