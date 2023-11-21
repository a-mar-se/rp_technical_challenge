from django.shortcuts import render
from django.http import HttpResponse


def validate(request):
    return HttpResponse("validating csv file...")

