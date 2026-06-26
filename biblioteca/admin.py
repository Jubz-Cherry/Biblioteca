from django.contrib import admin
from biblioteca.models import Author, Category, RegisterBooks, Userlogin

#face de admin do django

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'telephone')
    list_display_links = ('id', 'name')
    list_per_page = 20
    search_fields = ('name', 'telephone')


admin.site.register(Userlogin, UserAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 20
    search_fields = ('name',)

admin.site.register(Author, AuthorAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 20
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class RegisterBooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('id', 'title')
    list_per_page = 20
    search_fields = ('title', 'description')
    filter_horizontal = ('authors', 'categories')

admin.site.register(RegisterBooks, RegisterBooksAdmin)