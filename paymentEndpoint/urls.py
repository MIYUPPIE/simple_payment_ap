from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from api.views import PaymentViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Payment API",
        default_version='v1',
        description="API for payments",
    ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'payments', PaymentViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', csrf_exempt(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('', include(router.urls)),
]