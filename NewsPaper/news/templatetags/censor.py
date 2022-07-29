import json

from django import template

register = template.Library()


@register.filter()
def censor(in_text):
    with open('static/json/bad_words.json', 'r') as censor_file:
        bad_text = json.load(censor_file)

    for word in in_text.split():
        if word.lower() in bad_text:
            in_text = in_text.replace(
                word,
                f'{word[0]}{"*" * (len(word) - 1)}'
            )
    return in_text
