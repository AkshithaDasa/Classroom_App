from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin #as BaseUserAdmin
# class UserAdmin(BaseUserAdmin):
#     ordering = ['email']

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(AllotedCourse)
admin.site.register(Enrolled)