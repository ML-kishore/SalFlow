
    
import calendar
from django import template

register = template.Library()  # This line registers the tag library

@register.filter
def to_month_name(month_number):
    try:
        return calendar.month_abbr[int(month_number)]
    except (ValueError, IndexError, TypeError):
        return month_number