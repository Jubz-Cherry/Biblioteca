from django.contrib import admin
from django.urls import path
from biblioteca.views import BooksSearchView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("books/", BooksSearchView.as_view(), name="livros"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
