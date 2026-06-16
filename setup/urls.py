from django.contrib import admin
from django.urls import path
from biblioteca.views import livros_biblioteca



urlpatterns = [
    path('admin/', admin.site.urls),
    path('livros/', livros_biblioteca, name='livros_biblioteca'),

]
