from rest_framework import serializers
from testapp.models import Employee, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('department_name',)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('employee_name',
                  'department',
                  'joining_date',
                  'photo_file_name'
                  )
