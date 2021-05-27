from django.template.defaulttags import register
import ast


@register.filter
def get_item(dictionary, key):
    val = ast.literal_eval(dictionary)
    return val.get(key)
