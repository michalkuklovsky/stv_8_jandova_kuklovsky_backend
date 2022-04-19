from bokksapp.models import Users
from rest_framework.decorators import api_view
from bokksapp.custombackend import authenticate
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser


@api_view(['POST'])
def login(request):
    post_data = JSONParser().parse(request)
    try:
        del request.session['user']
    except:
        pass
    user = authenticate(request, post_data['email'], post_data['password'])
    if user is None:
        return JsonResponse({"error": {"message": "Invalid username or password"}}, status=401, safe=False)

    request.session['user'] = {"id": user.id, "email": user.email, "is_admin": user.is_admin}
    request.session['cart'] = []

    response = {"user": request.session['user']}
    return JsonResponse(response, status=200, safe=False)


@api_view(['POST'])
def logout(request):
    try:
        del request.session['user']
        del request.session['cart']
        return HttpResponse(status=204)
    except:
        response = {'error': {'message': 'Log out not successful'}}
        http_status = 400
        return JsonResponse(response, status=http_status, safe=False)


@api_view(['GET'])
def profile(request):
    if 'user' not in request.session:
        response = {'error': {'message': 'Unauthorized'}}
        http_status = 401
    else:
        response = {"user": request.session['user']}
        http_status = 200
    # elif request.session['user']['id']:
    #     response = {'error': {'message': 'Forbidden'}}
    #     http_status = 403
    # else:
    #     response = {'error': {'message': 'Unauthorized'}}
    #     http_status = 401
    return JsonResponse(response, status=http_status, safe=False)
