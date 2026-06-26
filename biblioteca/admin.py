from django.contrib import admin
from biblioteca.models import User

#face de admin do django

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'telephone')
    list_display_links = ('id', 'name')
    list_per_page = 20
    search_fields = ('name', 'telephone')


admin.site.register(User, UserAdmin)
