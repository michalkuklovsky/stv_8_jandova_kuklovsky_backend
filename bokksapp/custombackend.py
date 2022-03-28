from django.contrib.auth.backends import BaseBackend
from bokksapp.models import Users


def authenticate(request, email, password):
    user = Users.objects.filter(email=email).first()
    if user is None:
        return None
    if user.password == password:
        return user


def get_user(user_id):
    try:
        return Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return None
