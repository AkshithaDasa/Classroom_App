from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,is_staff=False, is_superuser=False, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=self.normalize_email(email),
                                is_active = True,
                                is_staff = True,
                                is_superuser = True,
                                **extra_fields)
        user.set_password(password)
        user.save()
        return user
        



class User(AbstractUser):
    GENDER = {
        "F": "Female",
        "M": "Male",
    }
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_join = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=10,blank=True)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER,blank=True)

    objects = UserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = 'Users'




class Student(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)

    def clean(self):
        existing_teacher = Teacher.objects.filter(user_id=self.user_id)
        if existing_teacher.exists():
             raise ValidationError("This user has already registered as Teacher")

    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'Students'



class Department(models.Model):
    department_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return str(self.department_name)
    
    class Meta:
        verbose_name_plural = 'Department'




class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_credits = models.IntegerField()
    course_duration = models.IntegerField()  # in months
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return str(self.course_name)

    class Meta:
        verbose_name_plural = 'Courses'




class Teacher(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.IntegerField(blank=True)
    married = models.BooleanField(default=False)
    department_id = models.ForeignKey(Department,on_delete = models.CASCADE,default='')

    def clean(self):
        existing_student = Student.objects.filter(user_id=self.user_id)
        if existing_student.exists():
             raise ValidationError("This user has already registered as student.")
        if self.salary <= 1000:
            raise ValidationError("Salary should be more than 1000")

    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'Teachers'




class Enrolled(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    course_start = models.DateField()

    def clean(self):
        existing_enrollment = Enrolled.objects.filter(student_id=self.student_id, course_id=self.course_id)
        if existing_enrollment.exists():
            raise ValidationError("Student is already enrolled in this course.")
        
    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'Enrolled'




class AllotedCourse(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def clean(self):
        existing_teaching = AllotedCourse.objects.filter(teacher_id=self.teacher_id, course_id=self.course_id)
        if existing_teaching.exists():
            raise ValidationError("Teacher is already teaching this course.")
        
    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'AllotedCourse'




class Assignment(models.Model):
    assigned_by = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank = True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'Assignment'



class Submission(models.Model):
    assignment_id = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'Submission'

