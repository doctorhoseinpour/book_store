from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)


class Employee(models.Model):
    employee_name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, to_field='department_name', on_delete=models.CASCADE)
    joining_date = models.DateField()
    photo_file_name = models.CharField(max_length=500)
