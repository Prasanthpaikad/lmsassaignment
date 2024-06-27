from django import template

register = template.Library()

@register.filter
def user_role(user):
   
    if user.is_authenticated:
        try:
            profile = user.userprofile  
            if profile.is_instructor:
                return "Instructor"
            else:
                return "Student"
        except CustomUser.DoesNotExist:
            pass
    return ""