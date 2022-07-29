from django import template

register = template.Library()


@register.simple_tag()
def news_pub_name(val, format_str='%d.%m.%Y'):
    return val.strftime(format_str)
