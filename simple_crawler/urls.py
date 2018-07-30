from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    #re_path(r'(?P<link>\w+)', views.result, name="result")
    path("<path:link>", views.result, name="result")
]