# Copyright (c) 2018, DjaoDjin inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Convenience module for access of survey app settings, which enforces
default settings when the main settings module does not contain
the appropriate settings.
"""
from django.conf import settings

_SETTINGS = {
    'AUTH_USER_MODEL': getattr(
        settings, 'AUTH_USER_MODEL', 'django.contrib.auth.models.User'),
    'ACCOUNT_LOOKUP_FIELD': 'username',
    'ACCOUNT_MODEL': getattr(
        settings, 'AUTH_USER_MODEL', 'django.contrib.auth.models.User'),
    'ACCOUNT_SERIALIZER': 'survey.api.serializers.AccountSerializer',
    'BELONGS_LOOKUP_FIELD': None,
    'BELONGS_MODEL': None,
    'BELONGS_SERIALIZER': None,
    'CORRECT_MARKER': '(correct)',
    'DEFAULT_FROM_EMAIL': getattr(settings, 'DEFAULT_FROM_EMAIL', None),
    'EXTRA_FIELD': None,
    'QUESTION_MODEL': 'survey.Question',
    'QUESTION_SERIALIZER': 'survey.api.serializers.QuestionDetailSerializer',
}
_SETTINGS.update(getattr(settings, 'SURVEY', {}))

AUTH_USER_MODEL = _SETTINGS.get('AUTH_USER_MODEL')
ACCOUNT_MODEL = _SETTINGS.get('ACCOUNT_MODEL')
ACCOUNT_LOOKUP_FIELD = _SETTINGS.get('ACCOUNT_LOOKUP_FIELD')
ACCOUNT_SERIALIZER = _SETTINGS.get('ACCOUNT_SERIALIZER')
BELONGS_LOOKUP_FIELD = (_SETTINGS.get('BELONGS_LOOKUP_FIELD')
    if _SETTINGS.get('BELONGS_LOOKUP_FIELD')
    else _SETTINGS.get('ACCOUNT_LOOKUP_FIELD'))
BELONGS_MODEL = (_SETTINGS.get('BELONGS_MODEL')
    if _SETTINGS.get('BELONGS_MODEL') else _SETTINGS.get('ACCOUNT_MODEL'))
BELONGS_SERIALIZER = (_SETTINGS.get('BELONGS_SERIALIZER')
    if _SETTINGS.get('BELONGS_SERIALIZER')
    else _SETTINGS.get('ACCOUNT_SERIALIZER'))
CORRECT_MARKER = _SETTINGS.get('CORRECT_MARKER')
DEFAULT_FROM_EMAIL = _SETTINGS.get('DEFAULT_FROM_EMAIL')
QUESTION_MODEL = _SETTINGS.get('QUESTION_MODEL')
QUESTION_SERIALIZER = _SETTINGS.get('QUESTION_SERIALIZER')

SLUG_RE = r'[a-zA-Z0-9-]+'
PATH_RE = r'([a-zA-Z0-9-]+(/[a-zA-Z0-9\-]+)*)?'
