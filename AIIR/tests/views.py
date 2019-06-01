# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from models import Student
from django.core import serializers
import json
import datetime
# Create your views here.

def index(request):
    
    fs = open(os.getcwd()+"/tests/views/plik.html","r+")
    return HttpResponse(fs)


def nowa(request):

    a = Student.objects.filter(id=1)
    serialised = serializers.serialize('json', a)

    return HttpResponse(a)

def create_new_task(request):
    response = request.body
    response = json.loads(response)

    # boolean
    random = response["random"]
    # str
    if random is False:
        # dostajemy dane wejsciowe -> zapisujemy je do pliku -> uruchom klastrowanie
        data = response["data"]
    # w przeciwym wypadku wygeneruj dane -> zapisz do pliku -> wyslij 
    # str
    login = response["login"]
    print(response)
    # do usuniecia
    return HttpResponse([random, data, login]) 

def nodeInfo(request):
    response = {}
    response["id"] = 123
    response["status"] = 1
    response = json.dumps(response)
    return HttpResponse(response)

def input_data (request, input, taskId):
    response = {}
    response['data'] = "test_input_data"
    response = json.dumps(response)
    return HttpResponse(response)

def output_data (request, input, taskId):
    response = {}
    response['data'] = "test_output_data"
    response = json.dumps(response)
    return HttpResponse(response)

def tasks(request, login):
    tasks = []
    
    task = {}
    task["id"] = 123
    task["status"] = 2
    task_datetime = datetime.datetime.now()
    task_datetime = str(task_datetime)[:-7]
    task["date"] = task_datetime
    task["type"] = "random"
    task["progress"] = 101
    tasks.append(task)
    
    response = {}
    response = json.dumps(tasks)

    return HttpResponse(response)