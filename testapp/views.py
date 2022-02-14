from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db import IntegrityError
from testapp.models import Employee, Department
from testapp.serializers import EmployeeSerializer, DepartmentSerializer
import json


@csrf_exempt
def department_api(request, department_name=''):
    if request.method == 'GET':
        departments = Department.objects.all()
        departments_serialized = DepartmentSerializer(departments, many=True)
        return JsonResponse(departments_serialized.data, safe=False)
    elif request.method == 'POST':
        department_data = JSONParser().parse(request)
        department_serialized = DepartmentSerializer(data=department_data)
        if department_serialized.is_valid():
            department_serialized.save()
            return JsonResponse(f"department {department_data['department_name']} added successfully", safe=False)
        return JsonResponse(f"failed to add requested department!", safe=False)
    elif request.method == 'PUT':
        req_body = json.loads(request.body)
        department = Department.objects.get(department_name=req_body['old_dept_name'])
        new_dept_name = req_body['new_dept_name']
        department.department_name = new_dept_name
        try:
            department.save()
            return JsonResponse('update was successful', safe=False)
        except IntegrityError:
            return JsonResponse("integrity error occurred while updating")
    elif request.method == 'DELETE':
        department = Department.objects.get(department_name=department_name)
        department.delete()
        return JsonResponse("deleted successfully!", safe=False)
