from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene un valor del diccionario usando una clave."""
    return dictionary.get(key)
