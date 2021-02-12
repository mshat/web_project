from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
# from mainapp.api import MyUserViewSet
#
#
# router = routers.DefaultRouter()
# router.register('api/v1/users/', MyUserViewSet, 'users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('mainapp.urls')),
    path('', include('mainapp.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/token_auth/', include('djoser.urls.authtoken')),
    path('api/v1/base_auth/', include('rest_framework.urls')),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)), # Перенаправляет запросы с корневового URL, на URL приложения
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Используется static() чтобы добавить соотношения для статических файлов. Только на период разработки




