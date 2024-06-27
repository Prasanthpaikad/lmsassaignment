from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Course,Lesson,Module,video,PDF


class UserRegisterForm(UserCreationForm):
 
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('instructor', 'Instructor'), ('student', 'Student')], required=True, label='Role')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'role']
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration','course_image','category']


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['module', 'name']
class VideoForm(forms.ModelForm):
    class Meta:
        model = video
        fields = ['title','serial_number','thumbnail', 'youtube_id', 'time_duration', 'preview', 'order']

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['file', 'order']

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'name']

class EnrollCourseForm(forms.Form):
    course_id = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput())

