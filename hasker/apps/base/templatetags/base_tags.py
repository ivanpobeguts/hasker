from django import template

from hasker.apps.questions.models import Question

register = template.Library()


@register.inclusion_tag("tags/trending.html")
def top_questions(n=5):
    return {'top_questions': Question.trending(n)}