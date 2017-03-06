from django.template.defaultfilters import register

@register.filter
def color_panel_heading(value):
    if value == 3:
        return 'panel-info'
    elif value == 4:
        return 'panel-success'

    return 'panel-default'
