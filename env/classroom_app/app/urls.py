from django.urls import path
from . import views

urlpatterns = [
    #login and logout urls
    path('login', views.LoginAPIView().as_view(),name='login'),
    path('logout', views.LogoutAPIView().as_view(),name='logout'),
    #register (create) urls
    path('register-admin',views.UsersCreateView().as_view(),name='users-register'),
    path('register-student',views.StudentCreateView().as_view(),name='studentregister'),
    path('register-teacher',views.TeacherCreateView().as_view(),name='student-register'),
    path('create-course',views.CourseCreateView.as_view(),name='course-create'),
    path('create-allotedcourse',views.AllotedCourseCreateView.as_view(),name='teachercourse-register'),
    path('create-enrolled',views.EnrolledCreateView.as_view(),name='studentcourse-register'),
    #List urls
    path('users',views.UsersListView().as_view(),name='users-info'),
    path('student',views.StudentListView.as_view(),name='student_info'),
    path('teacher',views.TeacherListView.as_view(),name='teacher-info'),
    path('course',views.CourseListView.as_view(),name='course-info'),
    path('allotedcourse',views.AllotedCourseListView.as_view(),name='teachercourse-info'),
    path('enrolled',views.EnrolledListView.as_view(),name='studentcourse-info'),
    #detail urls
    path('users/<int:pk>',views.UsersDetailView().as_view(),name='users-detailinfo'),
    path('student/<int:pk>',views.StudentDetailView.as_view(),name='student_detailinfo'),
    path('teacher/<int:pk>',views.TeacherDetailView.as_view(),name='teacher-detailinfo'),
    path('course/<int:pk>',views.CourseDetailView.as_view(),name='course-detailinfo'),
    path('allotedcourse/<int:pk>',views.AllotedCourseDetailView.as_view(),name='teachercourse-detailinfo'),
    path('enrolled/<int:pk>',views.EnrolledDetailView.as_view(),name='studentcourse-detailinfo'),

]