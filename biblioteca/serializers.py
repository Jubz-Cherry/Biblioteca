from rest_framework import serializers
from .models import Userlogin, RegisterBooks, Author, Category

class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userlogin
        fields = [
            'id',
            'name',
            'email',
            'telephone',
        ]

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class RegisterBooksSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = RegisterBooks
        fields = ['id', 'title', 'authors', 'description', 'categories']

    def create(self, validated_data):
        authors_data = validated_data.pop('authors', [])
        categories_data = validated_data.pop('categories', [])

        book = RegisterBooks.objects.create(**validated_data)

        for author in authors_data:
            author_obj, _ = Author.objects.get_or_create(name=author['name'])
            book.authors.add(author_obj)

        for category in categories_data:
            category_obj, _ = Category.objects.get_or_create(name=category['name'])
            book.categories.add(category_obj)

        return book