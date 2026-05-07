from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#    openapi.Info(
#       title="CHUPA ku CHUPA API",
#       default_version='v1',
#       description="API documentation for CHUPA ku CHUPA Bar & Lounge",
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls', namespace='products')),
    path('orders/', include('orders.urls')),
    path('bookings/', include('bookings.urls')),
    path('api/', include('api.urls')),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json')),
    path('service-worker.js', TemplateView.as_view(template_name='service-worker.js', content_type='application/javascript')),
    path('', include('products.urls', namespace='home')), # Set products as home for now
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
