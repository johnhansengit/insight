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

            # Check for True or False values
            if value is True:
                return 'yes'
            if value is False:
                return 'no'

            # Check for integer values
            ratings = {1: 'poor', 2: 'meh', 3: 'fine', 4: 'good', 5: 'excellent'}
            if value in ratings:
                return ratings[value]

    return []

