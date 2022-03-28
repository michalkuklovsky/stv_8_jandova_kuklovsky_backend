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
        return HttpResponse(status=204)
    except:
        response = {'errors': {'message': 'Logout not successful'}}
        http_status = 400
        return JsonResponse(response, status=http_status, safe=False)


@api_view(['GET', ])
def profile(request, id):
    if 'user' not in request.session:
        response = {'errors': {'message': 'Unauthorized'}}
        http_status = 401
    elif request.session['user']['id'] == id:
        response = {"user": request.session['user']}
        http_status = 200
    elif request.session['user']['id']:
        response = {'errors': {'message': 'Forbidden'}}
        http_status = 403
    else:
        response = {'errors': {'message': 'Unauthorized'}}
        http_status = 401
    return JsonResponse(response, status=http_status)
