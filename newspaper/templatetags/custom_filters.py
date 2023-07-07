from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value, arg):
    if arg not in str(value):
        return str(value)
    else:
        raise ValueError(f'Нельзя использовать нецензурную лексику {arg}')
