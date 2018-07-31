from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path("parsed_(http://)?(?P<link>.*)", views.result, name="result")
]