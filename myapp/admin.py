from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Categories)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(video)
admin.site.register(PDF)
admin.site.register(StudentEnrolCourse)