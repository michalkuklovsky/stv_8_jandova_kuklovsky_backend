from datetime import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from django.db.models import F


from bokksapp.models import Events
from bokksapp.models import Users

eventsGetColumns = ['id', 'name', 'description', 'img_path', 'user__id', 'user__email']
eventsPostColumns = ['name', 'description', 'img_path', 'user__id']
eventsAdminColumns = ['id', 'name', 'description', 'img_path', 'created_at', 'updated_at', 'deleted_at', 'user__id', 'user__email']


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
    response = {'events': list(page),
                'metadata': {
                    'page': int(parameters['page']),
                    'per_page': int(parameters['per_page']),
                    'pages': paginator.num_pages,
                    'total': paginator.count,
                    }
                }
    return response


def get_query(parameters):
    response = Events.objects.values(*eventsGetColumns).order_by(F('id').asc(nulls_last=True))

    paginator = Paginator(response, parameters['per_page'])

    if paginator.num_pages >= int(parameters['page']):
        page = paginator.get_page(parameters['page'])
    else:
        page = []

    return page, paginator


reasons = ['required', 'null string not allowed', 'img_path provided but file is missing', 'image provided but img_path is missing']

# POST /events endpoint
def postEvents(request):
    new_item = parse_request(request)

    if 'image' in request.FILES:
        file = request.FILES['image']
    else:
        file = None

    errors, response = check_post_body(request, new_item, file)
    if errors:
        return {'errors': errors}, 422

    newEvent = Events.objects.create(**new_item)
    if file is not None and new_item['img_path'] is not None:
        handle_uploaded_file(file, new_item['img_path'], 'events')

    response_dict = Events.objects.filter(id=newEvent.id).values(*eventsAdminColumns).first()

    return {'event': response_dict}, 201

def parse_request(request):
    r = request.POST
    return {
        'name': r.get('name'),
        'description': r.get('description'),
        'img_path': r.get('img_path')
    }

    # checks parameters in POST requst body and handles errors
def check_post_body(request, new_item, file):
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
        else:
            if file is None:
                errors.append({'field': 'image', 'reasons': [reasons[2]]})

    if file is not None and new_item['img_path'] is None:
        errors.append({'field': 'image', 'reasons': [reasons[3]]})

    if 'description' in new_item and new_item['description'] is not None:
        if new_item['description'] == '':
            errors.append({'field': 'name', 'reasons': [reasons[1]]})

    new_item['user'] = Users.objects.filter(id=request.session['user']['id']).first()

    response = dict(new_item)

    return errors, response

# https://docs.djangoproject.com/en/4.0/topics/http/file-uploads/
def handle_uploaded_file(f, name, res):
    with open(f'./bokksapp/resources/{res}/{name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@api_view(['GET', 'POST'])
def processRequest(request):
    if 'user' not in request.session:
        response = {'error': {'message': 'Unauthorized'}}
        http_status = 401
        return JsonResponse(response, status=http_status, safe=False)

    if not request.session['user']['is_admin']:
        response = {'error': {'message': 'Forbidden'}}
        http_status = 403
        return JsonResponse(response, status=http_status, safe=False)

    if request.method == 'GET':
        response, http_status = getEvents(request)
    elif request.method == 'POST':
        response, http_status = postEvents(request)
    else:
        response = {'error': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status, safe=False)
