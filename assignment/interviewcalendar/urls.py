from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('api/<int:pk>', views.UserUpdate.as_view(), name='slots_update'),
    re_path(r'^api/(?P<pk>[0-9]+)/dates/$', views.dates_list, name='get_slots'),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
