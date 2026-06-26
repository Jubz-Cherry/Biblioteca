from django.contrib import admin
from django.urls import path, include
from biblioteca.views import BooksSearchView, UserloginView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'userlogin', UserloginView, basename='userlogin')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("books/", BooksSearchView.as_view(), name="livros"),
    
    path('login/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
