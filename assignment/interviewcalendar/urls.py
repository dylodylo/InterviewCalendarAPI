from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/<int:pk>', views.UserUpdate.as_view()),
    re_path(r'^users/(?P<pk>[0-9]+)/dates/$', views.dates_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)