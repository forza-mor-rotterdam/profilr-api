from django.http import HttpResponse
from django.urls import path


def http_response(request):
    return HttpResponse("<h1>Hello</h1>")


urlpatterns = [
    path("hello", http_response, name="http_response"),
]
