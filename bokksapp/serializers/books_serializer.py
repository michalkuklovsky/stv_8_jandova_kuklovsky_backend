from rest_framework import serializers
from ..models import Authors, Books, Genres


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('id', 'name')


class PutBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = '__all__'


class PostBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = ('id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path', 'quantity', 'authors', 'genres')

