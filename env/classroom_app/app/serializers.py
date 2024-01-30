from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
    
    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key



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
        with transaction.atomic():
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
        user_data = data.pop('user_id')

        
        with transaction.atomic():
            user_instance = User.objects.create(**user_data)
            teacher_instance = Teacher.objects.create(user_id=user_instance, **data)
        return teacher_instance
     


class CourseSerializer(serializers.ModelSerializer):
    # instructor_id = TeacherSerializer(read_only=True, many=True)
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
        