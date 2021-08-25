import re

from django.core.exceptions import ValidationError


def hex_valid(hex_string):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_string)
    if match:
        return hex_string
    else:
        raise ValidationError("Введите HEX значение")


def recipe_time_valid(value):
    if value >= 1:
        return value
    else:
        raise ValidationError("Приготовление не может занимать "
                              "меньше одной минуты")
