from django import template

register = template.Library()

@register.filter(name='get_emotions')
def get_emotions(emotions_by_date, date):
    for entry in emotions_by_date:
        if entry['date'] == date:
            print(entry['emotions'])
            return entry['emotions']
    return []
