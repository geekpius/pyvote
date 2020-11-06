from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(big_number, small_number):
    return big_number-small_number
    