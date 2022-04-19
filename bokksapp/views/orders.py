from datetime import datetime
import json
from urllib import request

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from django.db.models import F


from bokksapp.models import Orders
from bokksapp.models import Users
from bokksapp.models import Books


ordersGetColumns = ['id', 'total_sum', 'payment_type', 'shipping_type', 'status', 'created_at', 'user__id', 'user__email']
ordersPostColumns = ['id', 'total_sum', 'payment_type', 'shipping_type', 'status', 'created_at', 'user__id', 'user__email']
booksGetColumns = ['id']



# GET /events endpoint
def getOrders(request):
    parameters = {}
    parameters['per_page'] = 20
    parameters['page'] = 1

    # creates query from parameteres
    page, paginator = get_query(request, parameters)

    response = serialize_object(parameters, page, paginator)

    return response, 200


# creates response for GET /events request
def serialize_object(parameters, page, paginator):
    response = {'orders': list(page),
                'metadata': {
                    'page': int(parameters['page']),
                    'per_page': int(parameters['per_page']),
                    'pages': paginator.num_pages,
                    'total': paginator.count,
                    }
                }
    return response


def get_query(request, parameters):
    userID = request.session['user']['id']
    response = Orders.objects.values(*ordersGetColumns).filter(user__id=userID).order_by(F('id').asc(nulls_last=True))

    paginator = Paginator(response, parameters['per_page'])

    if paginator.num_pages >= int(parameters['page']):
        page = paginator.get_page(parameters['page'])
    else:
        page = []

    return page, paginator


reasons = ['required', 'null string not allowed', 'img_path provided but file is missing', 'image provided but img_path is missing']

# POST /events endpoint
def postOrders(request):
    new_item = parse_request(request)

    errors, response = check_post_body(request, new_item)
    if errors:
        return {'errors': errors}, 422

    newOrder = Orders.objects.create(**new_item)

    response_dict = Orders.objects.filter(id=newOrder.id).values(*ordersPostColumns).first()

    return {'order': response_dict}, 201

def parse_request(request):
    r = request.POST
    return {
        'payment_type': r.get('description'),
        'shipping_type': r.get('img_path'),
        'status': r.get('name'),
    }

    # checks parameters in POST requst body and handles errors
def check_post_body(request, new_item, file):
    errors = []
    response = {}

    if 'payment_type' not in new_item:
        new_item['payment_type'] = None
        errors.append({'field': 'payment_type', 'reasons': [reasons[0]]})

    if 'shipping_type' not in new_item:
        new_item['shipping_type'] = None
        errors.append({'field': 'shipping_type', 'reasons': [reasons[0]]})

    if new_item['payment_type'] is not None:
        if new_item['payment_type'] == '':
            errors.append({'field': 'payment_type', 'reasons': [reasons[0], reasons[1]]})

    if new_item['shipping_type'] is not None:
        if new_item['shipping_type'] == '':
            errors.append({'field': 'shipping_type', 'reasons': [reasons[0], reasons[1]]})

    if new_item['status'] is not None:
        if new_item['status'] == '':
            errors.append({'field': 'status', 'reasons': [reasons[0], reasons[1]]})

    new_item['user'] = Users.objects.filter(id=request.session['user']['id']).first()

    bookIDs = []
    for i in request.session['cart']:
        thisID = Users.objects.values('id').filter(title=i['title']).first()
        bookIDs.append(thisID)

    new_item['books'] = Users.objects.filter(pk__in=bookIDs).all()

    response = dict(new_item)

    return errors, response

@api_view(['GET', 'POST'])
def processRequest(request):
    if 'user' not in request.session:
        response = {'error': {'message': 'Unauthorized'}}
        http_status = 401
        return JsonResponse(response, status=http_status, safe=False)

    if request.method == 'GET':
        response, http_status = getOrders(request)
    elif request.method == 'POST':
        response, http_status = postOrders(request)
    else:
        response = {'error': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)
