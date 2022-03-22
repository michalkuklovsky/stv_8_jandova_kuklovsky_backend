# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime


class Users(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    deleted_at = models.DateTimeField(blank=True, null=True)


class Authors(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    deleted_at = models.DateTimeField(blank=True, null=True)


class Genres(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    deleted_at = models.DateTimeField(blank=True, null=True)


class Books(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField()
    quantity = models.IntegerField()
    isbn = models.CharField(max_length=255)
    img_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    authors = models.ManyToManyField(Authors)
    genres = models.ManyToManyField(Genres)


class Orders(models.Model):
    total_sum = models.FloatField()
    payment_type = models.CharField(max_length=255)
    shipping_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    books = models.ManyToManyField(Books)


class Events(models.Model):
    name = models.CharField(max_length=255)
    img_path = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    deleted_at = models.DateTimeField(blank=True, null=True)