from django.shortcuts import render
from django.http import Http404

from .models import Element

def index(request):
    return render(request, "simple_crawler/index.html")

def result(request, element_id):
    data = Element.objects.order_by('content')[:5]
    return render(request, "simple_crawler/result.html", {"element_list": data})