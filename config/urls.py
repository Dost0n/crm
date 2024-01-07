from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from .views import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version="v1",
        description="Nasiya savdo",
        terms_of_services="CRM"
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/', include('investor.urls')),
    path('api/v1/payments/', include('payment.urls')),


    # swagger
    path('swagger/', schema_view.with_ui(
        "swagger", cache_timeout=0), name="swagger-swagger-ui"),
    path('redoc/', schema_view.with_ui(
        "redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
