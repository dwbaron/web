from django import template
import markdown

register = template.Library()


@register.filter
def get_digest(digest):

    new_digest = markdown.markdown(digest[:64],
                                   extensions=[
                                       'markdown.extensions.extra',
                                       'markdown.extensions.codehilite',
                                       'markdown.extensions.toc',
                                   ])
    return new_digest
