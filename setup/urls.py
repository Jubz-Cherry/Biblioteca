from django.contrib import admin
from django.urls import path, include
from biblioteca.views import BooksSearchView, RegisterBooksView, UserloginView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserloginView, basename='users')
router.register(r'registerbook', RegisterBooksView, basename='registerbook')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('books/', BooksSearchView.as_view(), name='books'),

    path('api/', include(router.urls)),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
