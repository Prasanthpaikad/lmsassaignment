
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import CustomUser,Categories,Course,StudentEnrolCourse
from django.db.models import Q 
from .forms import CourseForm,LessonForm,ModuleForm, VideoForm, PDFForm, EnrollCourseForm
from .models import Course,Module, video, PDF,Lesson
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
def index(request):
    course=Course.objects.all()
    categories = Course.objects.values_list('category', flat=True).distinct()
    context={
        'course': course,
        'categories':categories
    }
    
    return render(request,'home.html',context)

def register(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role')
            try:
                user.save()
            except ValidationError as e:
                form.add_error(None, e)  
                return render(request, 'register.html', {'form': form})
            
            token = default_token_generator.make_token(user)
            user_email = user.email
            link = request.build_absolute_uri('/verify-email/?token=' + token + '&user_id=' + str(user.id))
            send_mail(
                'Verify your account',
                'Follow this link to verify your account: ' + link,
                'your_email@example.com', 
                [user_email],
                fail_silently=False,
            )
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})



def loginprofile(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                try:
                    
                    
                    if user.role == 'instructor':
                        return redirect('mci') 
                    elif user.role == 'student':
                        return redirect('mcs')  
                except CustomUser.DoesNotExist:
                  
                    pass
                
           
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logoutview(request):
    logout(request)
    return redirect('login')
def verify_email(request):
    token = request.GET.get('token')
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)

    if default_token_generator.check_token(user, token):
        
        user.is_active = True
        user.save()
        return HttpResponse('Email verified successfully')
    else:
        return HttpResponse('Invalid verification link')


def filter_data(request):
    category_filter = request.GET.get('query', None)
    if category_filter:
        filtered_courses = Course.objects.filter(category=category_filter)
    else:
        filtered_courses = Course.objects.all()
  

    course_data = [{'title': course.title, 'description': course.description,'image': course.course_image.url} for course in filtered_courses]
    print("catff",course_data)
    return JsonResponse( course_data,safe=False)
    
def search(request):
    
    if request.method == 'GET':
        query = request.GET.get('query', '')
        print("qurey;;;",query)
        if query:
            courses = Course.objects.filter(title__icontains=query)
            print("courses1;;;",courses)
        else:
            courses = Course.objects.all()
            print("courses;;;",courses)

        results = [{'title': course.title, 'description': course.description, 'image': course.course_image.url} for course in courses]
        print("results",results)
        
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
@login_required
# @permission_required('myapp.can_create_course', raise_exception=True)
def course_create(request):
    if request.user.role == 'instructor':
        if request.method == 'POST':
            form = CourseForm(request.POST,request.FILES)
            if form.is_valid():
                course = form.save(commit=False)
                course.instructor = request.user 
                course.save()
                return redirect('mci')
            else:
                print(form.errors)   
        else:
            form = CourseForm()
        return render(request, 'instructer/createcourse.html', {'form': form})
    else:
        messages.warning(request, "You have no permission to create course")
@login_required
def coursedetail_stud(request,pk):

    course = get_object_or_404(Course, pk=pk)

    
    modules = Module.objects.filter(course=course)
    
    course_content = []
    for module in modules:
        lessons = Lesson.objects.filter(module=module)
        
        module_content = []
        for lesson in lessons:
            videos = video.objects.filter(lesson=lesson)
            pdfs = PDF.objects.filter(lesson=lesson)
            
           
            content = sorted(
                list(videos) + list(pdfs), 
                key=lambda x: x.order
            )
            
            module_content.append({
                'lesson': lesson,
                'content': content
            })
        
        course_content.append({
            'module': module,
            'lessons': module_content
        })

    return render(request,'dummy.html', {'course': course, 'course_content': course_content})
@login_required
def createlesson(request,module_id):
    if request.user.role == 'instructor':
        if request.method == 'POST':
            form = LessonForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.module_id = module_id
                lesson.save()
                return redirect('cdi', pk= module_id)
        else:
            form = LessonForm()
        return render(request, 'instructer/createlesson.html', {'form': form})
@login_required    
def createmodule(request,course_id):
    if request.user.role == 'instructor':
        if request.method == 'POST':
            form = ModuleForm(request.POST)
            
            if form.is_valid():
                module = form.save(commit=False)
                module.course_id = course_id
                module.save()
                return redirect('cdi',  pk=course_id)
        else:
            form = ModuleForm()

        return render(request,'instructer/createmodule.html', {'form': form})
def createcontent(request):
    return render(request,'instructer/createcontent.html')
def profile_stud(request):
    return render(request,'student/profile.html')


@login_required   
def coursedetail_inst(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    modules = Module.objects.filter(course=course)
    
    course_content = []
    for module in modules:
        lessons = Lesson.objects.filter(module=module)
        
        module_content = []
        for lesson in lessons:
            videos = video.objects.filter(lesson=lesson)
            pdfs = PDF.objects.filter(lesson=lesson)
            
           
            content = sorted(
                list(videos) + list(pdfs), 
                key=lambda x: x.order
            )
            
            module_content.append({
                'lesson': lesson,
                'content': content
            })
        
        course_content.append({
            'module': module,
            'lessons': module_content
        })
    
    return render(request, 'instructer/coursedetail.html', {'course': course, 'course_content': course_content})
@login_required
def mycourse_stud(request):
    categories = Course.objects.values_list('category', flat=True).distinct()
    course = StudentEnrolCourse.objects.filter(student = request.user)
    
   
    

    context = {
        
        'course': course,'categories':categories
    }
    return render(request,'student/mycourse.html',context)
@login_required
def mycourse_inst(request):
    categories = Course.objects.values_list('category', flat=True).distinct()
    course = Course.objects.all()
    context = {
        
        'course': course,'categories':categories
    }
    return render(request,'instructer/mycourse.html',context)
@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'instructor':
        if request.method == 'POST':
            form = CourseForm(request.POST,request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('cdi', pk=course.pk)
        else:
            form = CourseForm(instance=course)
        return render(request, 'instructer/course_update.html', {'form': form})
@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'instructor':
        if request.method == 'POST':
            course.delete()
            return redirect('mci')
        return render(request, 'instructer/course_delete.html', {'course': course})
@login_required
def create_content(request, lesson_id):
    VideoFormSet = modelformset_factory(video, form=VideoForm, extra=1)
    PDFFormSet = modelformset_factory(PDF, form=PDFForm, extra=1)
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user.role == 'instructor':
        if request.method == 'POST':
            video_formset = VideoFormSet(request.POST, request.FILES, queryset=video.objects.none())
            pdf_formset = PDFFormSet(request.POST, request.FILES, queryset=PDF.objects.none())
            
            if video_formset.is_valid() and pdf_formset.is_valid():
                for form in video_formset.cleaned_data:
                    if form:
                        video.objects.create(
                            lesson=lesson,
                            serial_number=form['serial_number'],
                            thumbnail=form['thumbnail'],
                            title=form['title'],
                            youtube_id=form['youtube_id'],
                            time_duration=form['time_duration'],
                            preview=form['preview'],
                            order=form['order']
                        )
                        
                for form in pdf_formset.cleaned_data:
                    if form:
                        PDF.objects.create(
                            lesson=lesson,
                            file=form['file'],
                            order=form['order']
                        )
                        
                return redirect('cdi', pk=lesson_id)
        else:
            video_formset = VideoFormSet(queryset=video.objects.none())
            pdf_formset = PDFFormSet(queryset=PDF.objects.none())

        return render(request, 'instructer/createcontent.html', {
            'lesson': lesson,
            'video_formset': video_formset,
            'pdf_formset': pdf_formset,
        })

def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    videos = video.objects.filter(lesson=lesson)
    pdfs = PDF.objects.filter(lesson=lesson)
    
    
    content = sorted(
        list(videos) + list(pdfs), 
        key=lambda x: x.order
    )
    
    return render(request, 'instructer/coursedetail.html', {'lesson': lesson, 'content': content})
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    

    if request.user.role != 'student':
        messages.error(request, "Only students can enroll in courses.")
        return redirect('cds', course_id=course.id)

    
    if StudentEnrolCourse.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
    else:
        
        enrollment = StudentEnrolCourse(student=request.user, course=course)
        enrollment.save()
        messages.success(request, "You have been enrolled in the course.")
    
    return redirect(reverse('cds', kwargs={'pk': course_id}))
@login_required
def profile(request):
    return render(request,'instructer/profile.html')

@login_required
def profile_update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        

        user = CustomUser.objects.get(id=user_id)

     
        
        user.username = username
        user.email = email

        if password:
            user.set_password(password)

        user.save()
      
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile' )
    
    
    
    
    
    


