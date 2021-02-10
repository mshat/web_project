from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('mainapp.urls')),
    path('api/v1/mainapp/', include('mainapp.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth_token/', include('djoser.urls.authtoken')),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)), # Перенаправляет запросы с корневового URL, на URL приложения
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Используется static() чтобы добавить соотношения для статических файлов. Только на период разработки




