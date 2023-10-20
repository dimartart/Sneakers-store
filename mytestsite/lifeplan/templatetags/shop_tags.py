from django import template
from lifeplan.models import *

register = template.Library()


@register.inclusion_tag('lifeplan/list_categories.html')
def show_categories(selected_category=0):
    categories = Category.objects.all()
    return {'categories': categories, 'selected_category': selected_category}