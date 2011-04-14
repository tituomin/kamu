#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections

from kamu.opinions.models import Question, Option, Answer, \
    VoteOptionCongruence, QuestionSessionRelevance, QuestionSource
from kamu.opinions.views import LAST_QUESTION_KEY
from kamu.votes.models import Party, Session, Member
from kamu.user_voting import models as user_voting
from django.contrib.contenttypes.models import ContentType
from kamu.opinions.views import get_promise_statistics_summary
from django.utils.translation import ugettext as _
from django import forms

from django import template
register = template.Library()

@register.inclusion_tag('opinions/promise_statistics_sidebar.html',
                        takes_context=True)
def promise_statistics_sidebar(context, opinions_page, user, question=None):
    args = get_promise_statistics_summary(user, question)
    args['opinions_page'] = opinions_page
    args['system_congruences'] = not VoteOptionCongruence.objects.user_has_congruences(user)
    return args

@register.filter
def congruence_to_percentage(share):
    if (share is None):
        return _("N/A")
    try:
        return "%i" % int((share+1)/2.0*100)
    except ValueError:
        return ''

@register.filter
def congruence_to_color(share):
    base = [0x90, 0x90, 0x90]
    percent = int((share + 1) / 2.0 * 100)
    percent *= 2
    lim = 50 * 2
    if percent < lim:
        base[0] += lim - percent
        base[1] -= lim - percent
        base[2] -= lim - percent
    else:
        base[0] -= percent - lim
        base[1] += percent - lim
        base[2] -= percent - lim
    return "#%02x%02x%02x" % tuple(base)

@register.inclusion_tag('opinions/match_session.html', takes_context=True)
def match_session(context, session, question=None, delete=False):
    src_list = QuestionSource.objects.all()
    args = dict(src_list=src_list, session=session, question=question,
                delete=delete)
    session = context['request'].session
    if session and LAST_QUESTION_KEY in session:
        act_que = session[LAST_QUESTION_KEY]
        args['active_question'] = act_que
        que = src_list[1].question_set.all()[0]

    return args
