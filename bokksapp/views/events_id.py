import json

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view



from bokksapp.models import Events
# from bokksapp.models import Users

eventsColumns = ['id', 'name', 'description', 'img_path', 'user__id', 'user__email']

# GET /events/{id} endpoint
def get_id(request, id):
    event = Events.objects.values(*eventsColumns).filter(pk=id, deleted_at__isnull=True).first()
    if event is None:
        return {'error': {'message': 'Zaznam neexistuje'}}, 404
        
    # if event['deleted_at'] is not None:
    #     return {'error': {'message': 'Zaznam neexistuje'}}, 404

    response = serialize_object('event', event)
    return response, 200

def serialize_object(str, get):
    return {str: get}


eventsPutColumns = ['name', 'description', 'img_path']
reasons = ['required', 'null string not allowed', 'not number']

# PUT /events/{id} endpoint
def put_id(request, id):
    new_item = {}
    new_item = json.loads(request.body)
    if new_item == {}:
        return {'errors': {'message': 'request body required'}}, 422
    errors, update = check_put_body(new_item)
    if errors:
        return {'errors': errors}, 422

    put = Events.objects.filter(id=id).first()
    if put is None:
        return {'errors': {'message': 'Zaznam neexistuje'}}, 404

    Events.objects.filter(id=id).update(**update)

    put = Events.objects.values(*eventsColumns).filter(id=id).first()
    return serialize_object('event', put), 201

# checks parameters in POST requst body and handles errors
def check_put_body(new_item):
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


    if new_item['description'] is not None:
        if new_item['description'] == '':
            errors.append({'field': 'name', 'reasons': [reasons[1]]})

    for x in eventsPutColumns:
        if new_item[x] is not None:
            update[x] = new_item[x]

    return errors, update


# delete /events/{id} endpoint
def delete_id(request, id):
    event = Events.objects.filter(id=id).first()
    if event is None:
        return {'errors': {'message': 'Zaznam neexistuje'}}, 404

    Events.objects.filter(id=id).update(deleted_at=timezone.now())

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