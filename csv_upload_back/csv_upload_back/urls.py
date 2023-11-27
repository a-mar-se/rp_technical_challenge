
from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("csv_validation/", include("csv_validation.urls")),
    path('openapi/', get_schema_view(
        title="School Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema')
   
    # path('docs/', TemplateView.as_view(
    #     template_name='documentation.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='swagger-ui'),
]
