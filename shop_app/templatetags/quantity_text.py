from django.template.defaultfilters import register

@register.filter
def quantity_to_text(value):
    return 'brak' if value == 0 else 'na wyczerpaniu' if value < 5 else 'dostępny'
