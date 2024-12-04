from django.shortcuts import render
from django.http import HttpResponse

def main(request, name):
    string = f'Привет {name}!'
    return HttpResponse(string)