import hashlib
import math
import random

from django import template
from django.utils.safestring import mark_safe

from votes.models import Election

register = template.Library()


@register.filter()
def sanitized_vote_count(vote: Election):
    value = vote.votes().count()
    if value <= 5:
        return mark_safe("&le; 5")
    else:
        return f"{math.floor(value/5)*5} - {math.ceil(value/5)*5}"


@register.simple_tag(takes_context=True)
def current_user_ticket(context, election: Election):
    try:
        return election.ticket_set.filter(member=context["user"].member.uni_id).first()
    except AttributeError:
        return None
