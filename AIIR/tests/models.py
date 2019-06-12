# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import django.utils

# Create your models here.

class Student(models.Model):
    login = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.login


class File(models.Model):
    filename = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return self.filename


class Task(models.Model):

    progress = models.IntegerField(null=True, default=0)
    tabu_length = models.IntegerField(null=True)
    iterations_without_improvement = models.IntegerField(null=True)
    iterations_of_tabu = models.IntegerField(null=True)
    start_date = models.DateTimeField(null=True, default=django.utils.timezone.now)
    score = models.IntegerField(null=True, default=0)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    File = models.ForeignKey(File, on_delete=models.CASCADE, null=True)
    result_file = models.ForeignKey("File", on_delete=models.CASCADE, null=True, related_name="result_file")

    def __str__(self):
        return str(self.id) + " " + str(self.progress) + " " + str(self.tabu_length) + " " + str(self.iterations_without_improvement) + " " + str(self.iterations_of_tabu) + " " + str(self.start_date) + " " + str(self.score) + " " + str(self.Student) + " " + str(self.File)
