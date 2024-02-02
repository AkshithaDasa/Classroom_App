from rest_framework import serializers
from .models import *
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, data):
        phone_number = data.get('phone_number', None)

        if phone_number and len(phone_number) != 10:
            raise ValidationError("Phone number should be of 10 digits")

        if len(data['password']) != 8:
            raise ValidationError("Password should be of 8 characters")

        password = data.pop('password')

        user = User(**data)
        user.set_password(password)  
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        user.auth_token = token

        return user


class StudentSerializer(serializers.ModelSerializer):
    user_id = UsersSerializer()
    class Meta:
        model = Student
        fields = '__all__'

    @transaction.atomic
    def create(self, data):
        user_data = data.pop('user_id')
        user_instance = User.objects.create(**user_data)
        student_instance = Student.objects.create(user_id=user_instance, **data)
    
        return student_instance


class TeacherSerializer(serializers.ModelSerializer):
    user_id = UsersSerializer()
    class Meta:
        model = Teacher
        fields = '__all__'

    @transaction.atomic
    def create(self, data):
        # import ipdb; ipdb.set_trace()
        user_data = data.pop('user_id')
        user_instance = User.objects.create(**user_data)
        teacher_instance = Teacher.objects.create(user_id=user_instance, **data)
        return teacher_instance
     


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        

class EnrolledSerializer(serializers.ModelSerializer):
    student_id = StudentSerializer()
    course_id = CourseSerializer()
    class Meta:
        model = Enrolled
        fields = '__all__'
        

class AllotedCourseSerializer(serializers.ModelSerializer):
    teacher_id = TeacherSerializer()
    course_id = CourseSerializer()
    class Meta:
        model = AllotedCourse
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    assigned_by = TeacherSerializer()
    course = CourseSerializer()
    salary = serializers.SerializerMethodField()
    def get_salary(self,instance):
        return instance.assigned_by.salary

    class Meta:
        model = Assignment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        else:
            pass


class SubmissionSerializer(serializers.ModelSerializer):
    assignment_id = AssignmentSerializer()
    student_id = StudentSerializer()

    class Meta:
        model = Assignment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
    