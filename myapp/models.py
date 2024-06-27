
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
  

    ROLE_CHOICES = [
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users')

    def clean(self):
        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError("Invalid role selected.")
    
    def save(self, *args, **kwargs):
        self.clean()  
        super(CustomUser, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.username


class Categories(models.Model):
    
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_image = models.ImageField(upload_to="image/",null=True)
    duration = models.PositiveIntegerField()
    title = models.CharField(max_length=500,unique=True)
    created_at = models.DateField(auto_now_add=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        permissions = (('can_create_course', 'Can Create Course'),)
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    
   

    def __str__(self):
        return self.name 
class video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="youtube/", null=True)
   
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title 
class PDF(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    file = models.FileField(upload_to='docs/')
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.file.name

class StudentEnrolCourse(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student.email} enrolled in {self.course.title}"
