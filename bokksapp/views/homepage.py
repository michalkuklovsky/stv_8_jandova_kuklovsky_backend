from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from bokksapp.models import Books, Events

@api_view(['GET'])
def homepage(request):
	if request.method == 'GET':
		books = Books.objects.values().filter(deleted_at__isnull=True).all()[:4]
		events = Events.objects.values().filter(deleted_at__isnull=True).all()[:2]
		return JsonResponse({'books': list(books), 'events': list(events)}, status=status.HTTP_200_OK, safe=False)
	return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

