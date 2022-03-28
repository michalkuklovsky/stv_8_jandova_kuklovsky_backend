import json

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from datetime import datetime




from bokksapp.models import Events
# from bokksapp.models import Users

eventsColumns = ['id', 'name', 'description', 'img_path', 'user__id', 'user__email']
eventsAdminColumns = ['id', 'name', 'description', 'img_path', 'created_at', 'updated_at', 'deleted_at', 'user__id', 'user__email']

# GET /events/{id} endpoint
def get_id(request, id):
    if 'user' in request.session and request.session['user']['is_admin']:
        event = Events.objects.values(*eventsAdminColumns).filter(pk=id).first()
    else:
        event = Events.objects.values(*eventsColumns).filter(pk=id, deleted_at__isnull=True).first()

    if event is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404

    response = serialize_object('event', event)
    return response, 200

def serialize_object(str, get):
    return {str: get}


eventsPutColumns = ['name', 'description', 'img_path', 'deleted_at']
reasons = ['required', 'null string not allowed', 'img_path provided but file is missing', 'image provided but img_path is missing']

# PUT /events/{id} endpoint
def put_id(request, id):
    if 'user' not in request.session:
        response = {'errors': {'message': 'Unauthorized'}}
        http_status = 401
        return response, http_status
    if not request.session['user']['is_admin']:
        response = {'errors': {'message': 'Forbidden'}}
        http_status = 403
        return response, http_status
    
    new_item = parse_request(request)

    if 'image' in request.FILES:
        file = request.FILES['image']
    else:
        file = None

    if new_item == {}:
        response = {'errors': {'message': 'request body required'}}
        http_status = 422
        return response, http_status

    errors, update = check_put_body(new_item, file)
    if errors:
        return {'errors': errors}, 422

    put = Events.objects.filter(id=id).first()
    if put is None:
        response = {'errors': {'message': 'Zaznam neexistuje'}}
        http_status = 404
        return response, http_status

    Events.objects.filter(id=id).update(**update)

    if file is not None and new_item['img_path'] is not None:
        handle_uploaded_file(file, new_item['img_path'])

    put = Events.objects.values(*eventsAdminColumns).filter(id=id).first()
    return serialize_object('event', put), 201

def parse_request(request):
    r = request.POST
    return {
        'name': r.get('name'),
        'description': r.get('description'),
        'img_path': r.get('img_path')
    }

# checks parameters in POST requst body and handles errors
def check_put_body(new_item, file):
    errors = []
    response = update = {}

    for x in eventsPutColumns:
        if x not in new_item:
            new_item[x] = None

    if new_item['name'] is not None:
        if new_item['name'] == '':
            errors.append({'field': 'name', 'reasons': [reasons[0], reasons[1]]})

    if new_item['img_path'] is not None:
        if new_item['img_path'] == '':
            errors.append({'field': 'img_path', 'reasons': [reasons[1]]})
        else:
            if file is None:
                errors.append({'field': 'image', 'reasons': [reasons[2]]})

    if file is not None and new_item['img_path'] is None:
        errors.append({'field': 'image', 'reasons': [reasons[3]]})

    if new_item['description'] is not None:
        if new_item['description'] == '':
            errors.append({'field': 'name', 'reasons': [reasons[1]]})
    
    new_item['updated_at'] = datetime.now()

    for x in eventsPutColumns:
        if new_item[x] is not None:
            if x == 'deleted_at' and new_item[x] == 'undelete':
                update[x] = None
            else:
                update[x] = new_item[x]

    return errors, update

# https://docs.djangoproject.com/en/4.0/topics/http/file-uploads/
def handle_uploaded_file(f, name):
    with open(f'./bokksapp/resources/events/{name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# delete /events/{id} endpoint
def delete_id(request, id):
    if 'user' not in request.session:
        response = {'errors': {'message': 'Unauthorized'}}
        http_status = 401
        return response, http_status
    if not request.session['user']['is_admin']:
        response = {'errors': {'message': 'Forbidden'}}
        http_status = 403
        return response, http_status

    event = Events.objects.filter(id=id).first()
    if event is None:
        return {'errors': {'message': 'Zaznam neexistuje'}}, 404

    Events.objects.filter(id=id).update(updated_at=timezone.now(), deleted_at=timezone.now())

    return {}, 204


@api_view(['GET', 'DELETE', 'PUT'])
def processRequest(request, id):
    if request.method == 'GET':
        response, http_status = get_id(request, id)
    elif request.method == 'PUT':
        response, http_status = put_id(request, id)
    elif request.method == 'DELETE':
        response, http_status = delete_id(request, id)
    else:
        response = {'errors': {'message': 'Bad request'}}
        http_status = 400
    return JsonResponse(response, status=http_status)    