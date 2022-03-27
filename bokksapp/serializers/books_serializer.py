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


class GetBooksSerializer(serializers.ModelSerializer):
    # authors__id = AuthorSerializer(source='id', many=True)
    # genres__id = GenreSerializer(source='id', many=True)

    class Meta:
        model = Books
        fields = ('id', 'title', 'price', 'release_year', 'description', 'isbn', 'img_path',
                  'authors', #'authors__name',
                  'genres')#, 'genres__name')


class PostBookSerializer(serializers.ModelSerializer):
    # authors = AuthorSerializer(source='authors_list', many=True)
    # genres = GenreSerializer(source='genres_list', many=True)
    # authors = serializers.RelatedField(many=True)
    # genres = serializers.RelatedField(many=True)

    class Meta:
        model = Books
        fields = '__all__'

