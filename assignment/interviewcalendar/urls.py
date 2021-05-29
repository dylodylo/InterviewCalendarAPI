from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('users/<int:pk>', views.UserUpdate.as_view()),
    re_path(r'^users/(?P<pk>[0-9]+)/dates/$', views.dates_list),
    path('users/schema', SpectacularAPIView.as_view(), name='schema'),
    path('users', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
