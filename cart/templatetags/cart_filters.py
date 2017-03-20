from django.template.defaultfilters import register

@register.filter(name='get_quantity')
def get_quantity(filed, value):
    return filed[str(value)]
