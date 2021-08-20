import re

from django.core.exceptions import ValidationError


def HEX_valid(HEX_string):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', HEX_string)
    if match:
        return HEX_string
    else:
        raise ValidationError("Введите HEX значение")


def ingredient_amount_valid(value):
    if value >= 1 and value != 0:
        return value
    else:
        raise ValidationError("Количество ингредиентов не может " +
                              "быть меньше одного")
