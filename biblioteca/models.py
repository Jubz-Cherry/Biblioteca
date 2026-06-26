from django.db import models

class Userlogin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} - {self.email}"
    

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class RegisterBooks(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name="books")
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name="books")

    def __str__(self):
        return self.title
