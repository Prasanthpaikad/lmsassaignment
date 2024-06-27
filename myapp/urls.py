from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("",views.index,name='home'),
    path('verify-email/',views.verify_email, name='verify-email'),
    path("coursedetail/student/<int:pk>/",views.coursedetail_stud,name='cds'),
    path("coursedetail_inst/<int:pk>/",views.coursedetail_inst,name='cdi'),
    path("createcourse",views.course_create,name='create'),
    path("createmodule/<int:course_id>/",views.createmodule,name='modulecreate'),
    path("createlesson/<int:module_id>/",views.createlesson,name='lessoncreate'),
    path('enroll_course/<int:course_id>/', views.enroll_course, name='enroll_course'),

    
    path("profile/",views.profile,name='profile'),
    path("profile/update",views.profile_update,name='profile_update'),
    
    path('search/',views.search, name='search'),
    
    path('filter-data/', views.filter_data, name="filter-data"),
   

    path("mycourse_stud",views.mycourse_stud,name='mcs'),
    path("mycourse_inst",views.mycourse_inst,name='mci'),
    path("courseupdate/<int:pk>/",views.course_update,name='courseupdate'),
    path("coursedelete/<int:pk>/",views.course_delete,name='coursedelete'),
    
    path('lesson/<int:lesson_id>/content/', views.create_content, name='create_content'),
    
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    
    path("register",views.register,name='register'),
    path("login",views.loginprofile,name='login'),
    path("logout",views.logoutview,name='logout'),
    path(
        "change-password/",
        auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
      path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
  
