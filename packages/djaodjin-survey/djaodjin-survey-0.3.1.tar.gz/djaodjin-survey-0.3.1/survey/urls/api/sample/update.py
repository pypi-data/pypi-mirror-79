# Copyright (c) 2020, DjaoDjin inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.conf.urls import url

from ....api.sample import (AnswerAPIView, SampleAPIView,
    SampleAnswersAPIView, SampleRecentCreateAPIView, SampleFreezeAPIView)
from ....settings import SLUG_RE, PATH_RE

urlpatterns = [
   url(r'^(?P<sample>%s)/freeze/(?P<path>%s)/?' % (SLUG_RE, PATH_RE),
       SampleFreezeAPIView.as_view(), name='survey_api_sample_freeze'),
   url(r'^(?P<sample>%s)/(?P<rank>\d+)/?' % SLUG_RE,
       AnswerAPIView.as_view(), name='survey_api_answer'),
   url(r'^(?P<sample>%s)/answers/(?P<path>%s)/?' % (SLUG_RE, PATH_RE),
       SampleAnswersAPIView.as_view(), name='survey_api_sample_answers'),
   url(r'^(?P<sample>%s)/?' % SLUG_RE,
       SampleAPIView.as_view(), name='survey_api_sample'),
   url(r'^$',
       SampleRecentCreateAPIView.as_view(), name='survey_api_sample_new'),
]
