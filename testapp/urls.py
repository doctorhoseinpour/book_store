from testapp import views
from django.urls import re_path
urlpatterns = [
    re_path(r'^departments$', views.department_api),
    re_path(r'^departments/(?P<department_name>[\w-]+)$', views.department_api)
]
