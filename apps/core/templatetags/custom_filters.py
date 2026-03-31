from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def replace(value, arg):
    if len(arg.split(',')) != 2:
        return value
    old, new = arg.split(',')
    return value.replace(old, new)
