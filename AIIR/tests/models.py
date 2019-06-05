# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
    login = models.CharField(max_length=100)

    def __str__(self):
        return self.login

class File(models.Model):
    filename = models.CharField(max_length=20)
    
    def __str__(self):
        return self.filename

class Task(models.Model):

    progress = models.IntegerField(null=True)
    tabu_length = models.IntegerField(null=True)
    iterations_without_improvement = models.IntegerField(null=True)
    iterations = models.IntegerField(null=True)
    start_date = models.DateTimeField(null=True)
    score = models.IntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    matrix_file = models.ForeignKey(File, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.progress + " " + self.tabu_length + " " + self.iterations_without_improvement + " " + self.iterations + " " + self.start_date.__str__ + " " + self.score + " " + self.student.login + " " + self.matrix_file.filename