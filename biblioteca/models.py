from django.db import models
from django.contrib.auth.models import AbstractUser


class Userlogin(AbstractUser):
    telephone = models.CharField(max_length=30)

    def __str__(self):
        return self.username


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
    authors = models.ManyToManyField(
        Author,
        related_name="books"
    )
    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )

    def __str__(self):
        return self.title


class Loanbook(models.Model):
    user = models.ForeignKey(
        Userlogin,
        on_delete=models.CASCADE,
        related_name="loans"
    )

    book = models.ForeignKey(
        RegisterBooks,
        on_delete=models.CASCADE,
        related_name="loans"
    )

    borrowed_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-borrowed_at"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

