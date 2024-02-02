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
from rest_framework.filters import OrderingFilter

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




###### Login ######
    
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

###### Logout #######
        
class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request, format=None):
        if request.user.is_authenticated:
            request.auth.delete()
            logout(request)
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

 

####### ListCreate Views ########
        
class UsersView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        else:
            return []

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination



class StudentView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return []
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination


class TeacherView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return []
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filterset_fields = '__all__'
    filter_backends = (OrderingFilter,)
    pagination_class = PageNumberPagination



class CourseView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = '__all__'
    filter_backends = (OrderingFilter,)
    pagination_class = PageNumberPagination



class AllotedCourseView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
    queryset = AllotedCourse.objects.all()
    serializer_class = AllotedCourseSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination


class EnrolledView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
    queryset = Enrolled.objects.all()
    serializer_class = EnrolledSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination


class AssignmentView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        else:
            return [IsAuthenticated()]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination
    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = AssignmentSerializer
    #     fields = 
    #     kwargs['fields'] = fields
    #     return serializer_class(*args, **kwargs)
    



class SubmissionView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsStudent()]
        else:
            return [IsTeacher(),IsAdminUser()]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = SubmissionSerializer
    #     fields = ['id', 'submission_time']
    #     kwargs['fields'] = fields
    #     return serializer_class(*args, **kwargs)
    


class DepartmentView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
    queryset = Department.objects.all()
    filterset_fields = '__all__'
    pagination_class = PageNumberPagination

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = DepartmentSerializer
    #     fields = 
    #     kwargs['fields'] = fields
    #     return serializer_class(*args, **kwargs)
    



###### Detail Views #######

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


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer