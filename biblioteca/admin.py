from django.contrib import admin
from biblioteca.models import (Author,Category,RegisterBooks,Userlogin,Loanbook,)


# Usuários
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "telephone")
    list_display_links = ("id", "username")
    search_fields = ("username", "telephone")
    list_per_page = 20


admin.site.register(Userlogin, UserAdmin)


# Autores
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_per_page = 20


admin.site.register(Author, AuthorAdmin)


# Categorias
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)


# Livros
class RegisterBooksAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "category")
    list_display_links = ("id", "title")
    search_fields = ("title", "description")
    list_filter = ("category",)
    filter_horizontal = ("authors",)
    list_per_page = 20


admin.site.register(RegisterBooks, RegisterBooksAdmin)


# Empréstimos
class LoanbookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "book",
        "borrowed_at",
        "due_date",
        "returned_at",
    )
    list_display_links = ("id", "user")
    search_fields = (
        "user__username",
        "book__title",
    )
    list_filter = (
        "borrowed_at",
        "returned_at",
    )
    list_per_page = 20


admin.site.register(Loanbook, LoanbookAdmin)
