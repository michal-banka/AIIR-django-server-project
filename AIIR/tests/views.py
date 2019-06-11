# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Student, File, Task
from django.core import serializers
from django.db.models import Q
import json
import datetime
import uuid
import re
# Create your views here.

hosts = ["10.182.29.234", "10.182.62.254"]


def index(request):
    response = request.body
    response = json.loads(response)

    login = response["login"]
    random = response["random"]
    tabu_length = response["tabuLength"]
    iterations_without_improvement = response["iterationsWithoutImprovement"]
    iterations_of_tabu = response["iterationsOfTabu"]
    data = response["data"]

    if random is True:
        # todo
        data = create_data()

    matrix_filename = save_data_to_file(data)
    file_ = db_insert_file(matrix_filename)
    student = db_insert_student(login)
    task = create_task(tabu_length, iterations_of_tabu,
                       iterations_without_improvement, student, file_)
    task = db_insert_task(task)


def nowa(request):

    a = Student.objects.filter(id=1)
    serialised = serializers.serialize('json', a)

    return HttpResponse(a)


def create_new_task(request):
    response = request.body
    response = json.loads(response)

    login = response["login"]
    random = response["random"]
    tabu_length = response["tabuLength"]
    iterations_without_improvement = response["iterationsWithoutImprovement"]
    iterations_of_tabu = response["iterationsOfTabu"]
    data = response["data"]

    if random is True:
        # todo
        data = create_data()

    matrix_filename = save_data_to_file(data)
    file_ = db_insert_file(matrix_filename)
    student = db_insert_student(login)
    task = create_task(tabu_length, iterations_of_tabu,
                       iterations_without_improvement, student, file_)
    task = db_insert_task(task)

    for slave_id in range(1, len(hosts)):
        args = prepare_cluster_arguments(task, slave_id)
        os.system(
            "python3 /home/michal/Workspace/AIIR/AIIR/tests/distribute_single.py" + args)




def nodeInfo(request):
    # tasks = Task.objects.filter(~Q(progress=100))
    # for task in tasks:
    #     print(task)
    #     exists = os.path.isfile('/home/michal/Workspace/AIIR/AIIR/tests/data/results/')

    
    # regex = re.compile("^")
    # nodes = []
    # response = {}
    # response["id"] = 123
    # response["status"] = 1
    # nodes.append(response)

    # response = json.dumps(nodes)
    return HttpResponse("Keep out")


def input_data(request, input, taskId):
    task = Task.objects.filter(id=taskId).first()
    
    f = open("/home/michal/Workspace/AIIR/AIIR/tests/data/matrices/" + task.File.filename + ".txt", "r")
    response = {}
    response['data'] = f
    response = json.dumps(response)
    return HttpResponse(response)


def output_data(request, input, taskId):
    response = {}
    response['data'] = "test_output_data"
    response = json.dumps(response)
    return HttpResponse(response)


def tasks(request, login):
    response = Task.objects.all()
    response = serializers.serialize('json', response)
    return HttpResponse(response, content_type='application/json')


# NON CONTROLLER FUNCTIONS
def save_data_to_file(data):
    filename = uuid.uuid4()
    f = open("/home/michal/Workspace/AIIR/AIIR/tests/data/matrices/" +
             str(filename)+".txt", "w+")
    f.write(data)
    f.close()
    return filename


def prepare_cluster_arguments(task, node_id):
    arguments = [task.tabu_length, task.iterations_without_improvement, task.File.filename,
                 "result.txt", task.iterations_of_tabu, node_id, len(hosts), task.id, hosts[node_id]]
    result = ""
    for arg in arguments:
        result += " " + str(arg)
    return result


def create_task(tabu_length, iterations_of_tabu, iterations_without_improvement, student, file_):
    task = Task()
    task.tabu_length = tabu_length
    task.iterations_of_tabu = iterations_of_tabu
    task.iterations_without_improvement = iterations_without_improvement
    task.progress = 0
    task.score = 0
    task.start_date = datetime.datetime.now()
    task.Student = student
    task.File = file_
    return task


def create_data():
    return 0

# DATABASE FUNCTIONS

    # File


def db_insert_file(insert_filename):
    file_ = File()
    file_.filename = insert_filename
    file_.save()
    return file_

    # Student


def db_select_student(select_login):
    student = Student.objects.filter(login=select_login)
    student.login = select_login
    return student


def db_insert_student(insert_login):
    student = Student(login=insert_login)
    student.login = insert_login
    student.save()
    return student

    # Task


def db_insert_task(task):
    task.save()
    return task
