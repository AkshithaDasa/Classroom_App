from rest_framework import generics
from rest_framework.views import APIView, status
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import logout
from django.conf.urls import url

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return User.objects.filter(email=user.email).exists()

class IsStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        student = Student.objects.filter(user_id=user.id).first()
        if student and student.id == obj.id:
            return True
        return False

class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        teacher = Teacher.objects.filter(user_id=user.id).first()
        if teacher and teacher.id == obj.id:
            return True
        return False


#Login
def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user
    


class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        print(user.is_authenticated)
        return Response(data=data, status=status.HTTP_200_OK)


#Logout
class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request, format=None):
        if request.user.is_authenticated:
            request.auth.delete()
            logout(request)
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

# List Views

class UsersListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

class StudentListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

class TeacherListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

class AllotedCourseListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = AllotedCourse.objects.all()
    serializer_class = AllotedCourseSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

class EnrolledListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Enrolled.objects.all()
    serializer_class = EnrolledSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

#Create Views


class UsersCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherCreateView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class CourseCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrolledCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Enrolled.objects.all()
    serializer_class = EnrolledSerializer


class AllotedCourseCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = AllotedCourse.objects.all()
    serializer_class = AllotedCourseSerializer


#Detail Views

class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStudent]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTeacher]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrolledDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Enrolled.objects.all()
    serializer_class = EnrolledSerializer


class AllotedCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = AllotedCourse.objects.all()
    serializer_class = AllotedCourseSerializer