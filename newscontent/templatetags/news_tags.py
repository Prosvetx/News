from django import template
from django.db.models import Count
from ..models import Section

register = template.Library()

@register.simple_tag
def get_most_commented_posts():
    d = {}
    for section in Section.objects.annotate(cnt=Count('new')):
        d.update({section.title: section.cnt})
    return d

# @register.simple_tag
# def rng(number):
#     return list(i for i in range(int(number)))

@register.filter(name='times') 
def times(number):
    return range(number)
