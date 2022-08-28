import json

from django import template
from django.utils import timezone

register = template.Library()


@register.filter()
def censor(in_text):
    censured_text = in_text

    with open('static/json/bad_words.json', 'r') as censor_file:
        bad_text = json.load(censor_file)

    for word in censured_text.split():
        if word.lower() in bad_text:
            censured_text = censured_text.replace(
                word,
                f'{word[0]}{"*" * (len(word) - 1)}'
            )
    return censured_text


@register.filter()
def liter(in_word):
    return f'{in_word[:-1]}и'


@register.filter()
def name_month(val):
    val_obj = timezone.datetime.strptime(str(val), "%m")
    val_name = val_obj.strftime("%B")
    return val_name
