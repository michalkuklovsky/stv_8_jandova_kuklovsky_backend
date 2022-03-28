from datetime import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view


from bokksapp.models import Events
from bokksapp.models import Users

eventsGetColumns = ['id', 'name', 'description', 'img_path', 'user__id', 'user__email']
eventsPostColumns = ['name', 'description', 'img_path', 'user__id']

# GET /events endpoint
def getEvents(request):
    parameters = {}
    parameters['per_page'] = 20
    parameters['page'] = 1

    # creates query from parameteres
    page, paginator = get_query(parameters)

    response = serialize_object(parameters, page, paginator)

    return response, 200


# creates response for GET /events request
def serialize_object(parameters, page, paginator):
    response = {'items': list(page),
                'metadata': {
                    'page': int(parameters['page']),
                    'per_page': int(parameters['per_page']),
                    'pages': paginator.num_pages,
                    'total': paginator.count,
                    }
                }
    return response


def get_query(parameters):
    response = Events.objects.values(*eventsGetColumns)

    paginator = Paginator(response, parameters['per_page'])

    if paginator.num_pages >= int(parameters['page']):
        page = paginator.get_page(parameters['page'])
    else:
        page = []

    return page, paginator


reasons = ['required', 'null string not allowed', 'not number']

# POST /events endpoint
def postEvents(request):
    new_item = json.loads(request.body)
    errors, response = check_post_body(request, new_item)
    if errors:
        return {'errors': errors}, 422

    newEvent = Events.objects.create(**new_item)

    # user = Users.objects.filter(id=request.session['user']['id']).first()
    # newEvent.users.add(user)

    response_dict = {'id': newEvent.id}
    response_dict.update(response)
    del response_dict['user']
    response_dict['user__id'] = request.session['user']['id'] 
    response_dict['user__email'] = request.session['user']['email'] 

    return {'response': response_dict}, 201


    # checks parameters in POST requst body and handles errors
def check_post_body(request, new_item):
    errors = []
    response = {}

    if 'name' not in new_item:
        new_item['name'] = None
        errors.append({'field': 'name', 'reasons': [reasons[0]]})

    if new_item['name'] is not None:
        if new_item['name'] == '':
            errors.append({'field': 'name', 'reasons': [reasons[0], reasons[1]]})

    if 'img_path' in new_item and new_item['img_path'] is not None:
        if new_item['img_path'] == '':
            errors.append({'field': 'img_path', 'reasons': [reasons[1]]})

    if 'decription' in new_item and new_item['description'] is not None:
        if new_item['description'] == '':
            errors.append({'field': 'name', 'reasons': [reasons[1]]})

    new_item['user'] = Users.objects.filter(id=request.session['user']['id']).first()

    response = dict(new_item)

    return errors, response


@api_view(['GET', 'POST'])
def processRequest(request):
    if 'user' not in request.session:
        response = {'errors': {'message': 'Unauthorized'}}
        http_status = 401
        return JsonResponse(response, status=http_status, safe=False)

    if not request.session['user']['is_admin']:
        response = {'errors': {'message': 'Forbidden'}}
        http_status = 403
        return JsonResponse(response, status=http_status, safe=False)

    if request.method == 'GET':
        response, http_status = getEvents(request)
    elif request.method == 'POST':
        response, http_status = postEvents(request)
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)
