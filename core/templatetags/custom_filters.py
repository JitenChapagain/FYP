from django import template

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def get_item(dictionary, key):
    return dictionary.get(key)
