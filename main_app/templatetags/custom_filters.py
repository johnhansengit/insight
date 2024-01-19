from django import template

register = template.Library()

@register.filter(name='get_emotions')
def get_emotions(emotions_by_date, date):
    for entry in emotions_by_date:
        if entry['date'] == date:
            return entry['emotions']
    return []

@register.filter(name='get_lifestyle')
def get_lifestyle(lifestyle_by_date, date):
    for entry in lifestyle_by_date:
        if entry['date'] == date:
            value = entry['value']
            return value
    return []
