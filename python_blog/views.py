from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    name = 'Django'
    return HttpResponse('Hello World!')