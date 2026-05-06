from django import template
from main_blog.models import *

register = template.Library()

@register.simple_tag
def get_category():
    return Category.objects.all()

@register.inclusion_tag('list_category.html')
def show_category():
    cats = Category.objects.all()
    return {'cats': cats}