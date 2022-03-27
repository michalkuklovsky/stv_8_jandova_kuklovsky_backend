from bokksapp.models import Users
from rest_framework.decorators import api_view
from bokksapp.custombackend import authenticate
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser


@api_view(['POST', ])
def login(request):
    post_data = JSONParser().parse(request)

    user = authenticate(request, post_data['email'], post_data['password'])
    if user is None:
        return JsonResponse({"error": {"message": "Invalid user"}}, status=401, safe=False)

    request.session['user'] = {"id": user.id, "email": user.email, "is_admin": user.is_admin}

    return HttpResponse(status=204)


@api_view(['POST', ])
def logout(request):
    try:
        del request.session['user']
    except:
        return HttpResponse(status=400)
    return JsonResponse({"error": {"message": "Invalid user"}}, status=204, safe=False)


@api_view(['GET', ])
def profile(request, id):
    if request.session['user']['id'] == id:
        return JsonResponse({"user": request.session['user']}, status=200, safe=False)
    elif request.session['user']['id']:
        return HttpResponse(status=403)
    else:
        return HttpResponse(status=401)
