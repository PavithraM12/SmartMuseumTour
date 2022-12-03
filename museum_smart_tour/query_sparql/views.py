from django.shortcuts import render
from django.http import HttpResponse

def main_html(request):
    return render(request, "main.html")
    # return HttpResponse("Hello, world. You're at the polls index.")
