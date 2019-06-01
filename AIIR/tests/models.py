# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
    login = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.login + ' - ' + self.name


class File(models.Model):
    nameOfFile = models.CharField(max_length=20)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField()