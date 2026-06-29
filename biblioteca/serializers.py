from rest_framework import serializers
from .models import Userlogin, RegisterBooks, Author, Category


class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userlogin
        fields = [
            "id",
            "username",
            "email",
            "telephone",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Userlogin(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class RegisterBooksSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = RegisterBooks
        fields = [
            "id",
            "title",
            "authors",
            "description",
            "category",
        ]

    def create(self, validated_data):
        authors_data = validated_data.pop("authors", [])
        category_data = validated_data.pop("category")

        category, _ = Category.objects.get_or_create(
            name=category_data["name"]
        )

        book = RegisterBooks.objects.create(
            category=category,
            **validated_data
        )

        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(
                name=author_data["name"]
            )
            book.authors.add(author)

        return book

    def update(self, instance, validated_data):
        authors_data = validated_data.pop("authors", None)
        category_data = validated_data.pop("category", None)

        if category_data:
            category, _ = Category.objects.get_or_create(
                name=category_data["name"]
            )
            instance.category = category

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description",
            instance.description
        )
        instance.save()

        if authors_data is not None:
            instance.authors.clear()

            for author_data in authors_data:
                author, _ = Author.objects.get_or_create(
                    name=author_data["name"]
                )
                instance.authors.add(author)

        return instance
