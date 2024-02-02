from django.urls import path
from . import views

urlpatterns = [
    # login and logout urls
    path('login', views.LoginAPIView().as_view(),name='login'),
    path('logout', views.LogoutAPIView().as_view(),name='logout'),

    #ListCreate urls
    path('users',views.UsersView().as_view(),name='users'),
    path('student',views.StudentView.as_view(),name='student'),
    path('teacher',views.TeacherView.as_view(),name='teacher'),
    path('course',views.CourseView.as_view(),name='course'),
    path('allotedcourse',views.AllotedCourseView.as_view(),name='teachercourse'),
    path('enrolled',views.EnrolledView.as_view(),name='studentcourse'),
    path('assignment',views.AssignmentView.as_view(),name='assignment'),
    path('submission',views.SubmissionView.as_view(),name='submission'),
    path('department',views.DepartmentView.as_view(),name='department'),

    #detail urls
    path('users/<int:pk>',views.UsersDetailView().as_view(),name='users-detail'),
    path('student/<int:pk>',views.StudentDetailView.as_view(),name='student_detail'),
    path('teacher/<int:pk>',views.TeacherDetailView.as_view(),name='teacher-detail'),
    path('course/<int:pk>',views.CourseDetailView.as_view(),name='course-detail'),
    path('allotedcourse/<int:pk>',views.AllotedCourseDetailView.as_view(),name='teachercourse-detail'),
    path('enrolled/<int:pk>',views.EnrolledDetailView.as_view(),name='studentcourse-detail'),
    path('assignment/<int:pk>',views.AssignmentDetailView.as_view(),name='assignment-detail'),
    path('submission/<int:pk>',views.SubmissionDetailView.as_view(),name='submission-detail'),
    path('department/<int:pk>',views.DepartmentDetailView.as_view(),name='department-detail'),
]