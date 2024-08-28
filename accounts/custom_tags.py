from django.template import Library
from .models import Function

register = Library()

@register.filter()
def in_team(things, team):
    return things.filter(team=team)

@register.filter()
def in_function(things, team):
    return things.filter(function__in= Function.objects.filter(team=team))