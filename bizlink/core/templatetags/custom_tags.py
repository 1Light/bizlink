from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """Usage: {{ value|startswith:"/owner/" }}"""
    return value.startswith(arg)
