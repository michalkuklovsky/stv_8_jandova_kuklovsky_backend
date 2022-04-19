import json

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from django.db.models import F

# GET /events endpoint
def getCart(request):
    cart = request.session['cart']

    if cart == {}:
        response = {}
        response_code = 204
    else:
        response = serialize_object(cart)
        response_code = 200

    return response, response_code


# creates response for GET /events request
def serialize_object(cart):
    response = {
        'cart': cart,
        }
    return response

reasons = ['required', 'null string not allowed', 'img_path provided but file is missing', 'image provided but img_path is missing']

def postCart(request):
    new_item = parse_request(request)
    errors = []

    for x in ['title', 'quantity', 'price']:
        if x not in new_item:
            errors.append({'field': x, 'reasons': [reasons[0]]})
    if errors:
        return {'errors': errors}, 422

    errors, response = check_post_body(new_item)
    if errors:
        return {'errors': errors}, 422

    addToCart = {
        'title': response['title'],
        'quantity': response['quantity'],
        'price': response['price']
    },
    
    request.session['cart'] += addToCart

    response_code = 201
    return response, response_code

def parse_request(request):
    r = request.data
    return {
        'title': r.get('title'),
        'quantity': r.get('quantity'),
        'price': r.get('price')
    }

def check_post_body(new_item):
    errors = []
    response = {}

    if new_item['title'] is not None:
        if new_item['title'] == '':
            errors.append({'field': 'title', 'reasons': [reasons[0]]})

    if new_item['quantity'] is not None:
        if new_item['quantity'] == '':
            errors.append({'field': 'quantity', 'reasons': [reasons[0], reasons[0]]})
        else:
            new_item['quantity'] = int(new_item['quantity'])

    if new_item['price'] is not None:
        if new_item['price'] == '':
            errors.append({'field': 'price', 'reasons': [reasons[0], reasons[0]]})
        else:
            new_item['price'] = float(new_item['price'])
    
    response = dict(new_item)

    return errors, response

@api_view(['GET', 'POST'])
def processRequest(request):
    if 'user' not in request.session:
        response = {'error': {'message': 'Unauthorized'}}
        http_status = 401
        return JsonResponse(response, status=http_status, safe=False)

    if request.method == 'GET':
        response, http_status = getCart(request)
    elif request.method == 'POST':
        response, http_status = postCart(request)
    else:
        response = {'error': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)