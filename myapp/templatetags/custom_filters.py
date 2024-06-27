from django import template
from myapp.models import video, PDF

register = template.Library()

@register.filter
def is_video(value):
    return isinstance(value, video)

@register.filter
def is_pdf(value):
    return isinstance(value, PDF)
