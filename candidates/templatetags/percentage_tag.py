from django import template

register = template.Library()


@register.simple_tag
def percentage(divisor, quotient, determiner):
    if determiner == 0:
        if divisor == 0:
            return 0
        else:
            return round((quotient/divisor)*100,2)
    else:
        if divisor == 0:
            return 0
        else:
            return round(((divisor-quotient)/divisor)*100,2)