# Copyright (c) 2019, DjaoDjin inc.
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

import datetime, random, uuid

from django.db import models, transaction, IntegrityError
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from . import settings
from .compat import import_string
from .utils import get_account_model, get_question_model


def get_extra_field_class():
    extra_class = settings._SETTINGS.get('EXTRA_FIELD')
    if extra_class is None:
        extra_class = models.TextField
    elif isinstance(extra_class, str):
        extra_class = import_string(extra_class)
    return extra_class


class SlugTitleMixin(object):
    """
    Generate a unique slug from title on ``save()`` when none is specified.
    """
    slug_field = 'slug'

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        if getattr(self, self.slug_field):
            # serializer will set created slug to '' instead of None.
            return super(SlugTitleMixin, self).save(
                force_insert=force_insert, force_update=force_update,
                using=using, update_fields=update_fields)
        max_length = self._meta.get_field(self.slug_field).max_length
        slug_base = slugify(self.title)
        if len(slug_base) > max_length:
            slug_base = slug_base[:max_length]
        setattr(self, self.slug_field, slug_base)
        for _ in range(1, 10):
            try:
                with transaction.atomic():
                    return super(SlugTitleMixin, self).save(
                        force_insert=force_insert, force_update=force_update,
                        using=using, update_fields=update_fields)
            except IntegrityError as err:
                if 'uniq' not in str(err).lower():
                    raise
                suffix = '-%s' % "".join([random.choice("abcdef0123456789")
                    for _ in range(7)])
                if len(slug_base) + len(suffix) > max_length:
                    setattr(self, self.slug_field,
                        slug_base[:(max_length - len(suffix))] + suffix)
                else:
                    setattr(self, self.slug_field, slug_base + suffix)
        raise ValidationError({'detail':
            "Unable to create a unique URL slug from title '%s'" % self.title})


@python_2_unicode_compatible
class Unit(models.Model):
    """
    Unit in which an ``Answer.measured`` value is collected.
    """

    SYSTEM_STANDARD = 0
    SYSTEM_IMPERIAL = 1
    SYSTEM_RANK = 2
    SYSTEM_ENUMERATED = 3
    SYSTEM_FREETEXT = 4

    SYSTEMS = [
            (SYSTEM_STANDARD, 'standard'),
            (SYSTEM_IMPERIAL, 'imperial'),
            (SYSTEM_RANK, 'rank'),
            (SYSTEM_ENUMERATED, 'enum'),
            (SYSTEM_FREETEXT, 'freetext'),
        ]

    NUMERICAL_SYSTEMS = [
        SYSTEM_STANDARD,
        SYSTEM_IMPERIAL,
        SYSTEM_RANK
    ]

    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    title = models.CharField(max_length=150)
    system = models.PositiveSmallIntegerField(
        choices=SYSTEMS, default=SYSTEM_STANDARD)

    def __str__(self):
        return str(self.slug)


@python_2_unicode_compatible
class Choice(models.Model):
    """
    Choice for a multiple choice question.
    """
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    rank = models.IntegerField(
        help_text=_("used to order choice when presenting a question"))
    text = models.TextField()
    descr = models.TextField()

    class Meta:
        unique_together = ('unit', 'rank')

    def __str__(self):
        return str(self.text)


@python_2_unicode_compatible
class Metric(models.Model):
    """
    Metric on a ``Question``.
    """
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    title = models.CharField(max_length=150)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.slug)


@python_2_unicode_compatible
class AbstractQuestion(SlugTitleMixin, models.Model):

    slug_field = 'path'

    INTEGER = 'integer'
    RADIO = 'radio'
    DROPDOWN = 'select'
    SELECT_MULTIPLE = 'checkbox'
    TEXT = 'text'

    QUESTION_TYPES = (
            (TEXT, 'text'),
            (RADIO, 'radio'),
            (DROPDOWN, 'dropdown'),
            (SELECT_MULTIPLE, 'Select Multiple'),
            (INTEGER, 'integer'),
    )

    class Meta:
        abstract = True

    path = models.CharField(max_length=1024, unique=True, db_index=True)
    title = models.CharField(max_length=50)
    text = models.TextField(
        help_text=_("Detailed description about the question"))
    question_type = models.CharField(
        max_length=9, choices=QUESTION_TYPES, default=RADIO,
        help_text=_("Choose the type of answser."))
    correct_answer = models.ForeignKey(Choice,
        null=True, on_delete=models.PROTECT, blank=True)
    default_metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    extra = get_extra_field_class()(null=True, blank=True)

    def __str__(self):
        return str(self.path)

    @property
    def choices(self):
        if self.default_metric.unit.system == Unit.SYSTEM_ENUMERATED:
            return [(choice.text, choice.descr if choice.descr else choice.text)
                for choice in Choice.objects.filter(
                    unit=self.default_metric.unit).order_by('rank')]
        return None

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        if not self.title:
            max_length = self._meta.get_field('title').max_length
            self.title = self.text[:max_length]
        return super(AbstractQuestion, self).save(
            force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields)

    def get_correct_answer(self):
        correct_answer_list = []
        if self.correct_answer:
            #pylint: disable=no-member
            correct_answer_list = [
                asw.strip() for asw in self.correct_answer.text.split('\n')]
        return correct_answer_list


@python_2_unicode_compatible
class Question(AbstractQuestion):

# XXX Before migration:
#    pass
# XXX After migration
    class Meta(AbstractQuestion.Meta):
        swappable = 'QUESTION_MODEL'

    def __str__(self):
        return str(self.path)


@python_2_unicode_compatible
class Campaign(SlugTitleMixin, models.Model):

    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(null=True)
    title = models.CharField(max_length=150,
        help_text=_("Enter a campaign title."))
    description = models.TextField(null=True, blank=True,
        help_text=_("This description will be displayed to interviewees."))
    account = models.ForeignKey(settings.BELONGS_MODEL,
        on_delete=models.PROTECT, null=True)
    active = models.BooleanField(default=False)
    quizz_mode = models.BooleanField(default=False,
        help_text=_("If checked, correct answser are required"))
    defaults_single_page = models.BooleanField(default=False,
        help_text=_("If checked, will display all questions on a single page,"\
" else there will be one question per page."))
    one_response_only = models.BooleanField(default=False,
        help_text=_("Only allows to answer campaign once."))
    questions = models.ManyToManyField(settings.QUESTION_MODEL,
        through='survey.EnumeratedQuestions', related_name='campaigns')
    extra = get_extra_field_class()(null=True)

    def __str__(self):
        return str(self.slug)

    def has_questions(self):
        return self.questions.exists()


@python_2_unicode_compatible
class EnumeratedQuestions(models.Model):

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    question = models.ForeignKey(settings.QUESTION_MODEL,
        on_delete=models.CASCADE)
    rank = models.IntegerField(
        help_text=_("used to order questions when presenting a campaign."))
    required = models.BooleanField(default=True,
        help_text=_("If checked, an answer is required"))

    class Meta:
        unique_together = ('campaign', 'rank')

    def __str__(self):
        return str(self.question.path)


class SampleManager(models.Manager):

    def create_for_account(self, account_name, **kwargs):
        account_lookup_kwargs = {settings.ACCOUNT_LOOKUP_FIELD: account_name}
        return self.create(account=get_account_model().objects.get(
                **account_lookup_kwargs), **kwargs)

    def get_score(self, sample): #pylint: disable=no-self-use
        answers = Answer.objects.populate(sample)
        nb_correct_answers = 0
        nb_questions = len(answers)
        for answer in answers:
            if answer.question.question_type == Question.RADIO:
                if answer.measured in answer.question.get_correct_answer():
                    nb_correct_answers += 1
            elif answer.question.question_type == Question.SELECT_MULTIPLE:
                multiple_choices = answer.get_multiple_choices()
                if not (set(multiple_choices)
                       ^ set(answer.question.get_correct_answer())):
                    # Perfect match
                    nb_correct_answers += 1

        # XXX Score will be computed incorrectly when some Answers are free
        # form text.
        if nb_questions > 0:
            score = (nb_correct_answers * 100) / nb_questions
        else:
            score = None
        return score, answers


@python_2_unicode_compatible
class Sample(models.Model):
    """
    Sample to a Campaign. A Sample is composed of multiple Answers
    to Questions.
    """
    objects = SampleManager()

    slug = models.SlugField(unique=True,
        help_text="Unique identifier for the sample. It can be used in a URL.")
    created_at = models.DateTimeField(auto_now_add=True,
        help_text="Date/time of creation (in ISO format)")
    campaign = models.ForeignKey(Campaign, null=True, on_delete=models.PROTECT)
    account = models.ForeignKey(settings.ACCOUNT_MODEL,
        null=True, on_delete=models.PROTECT, related_name='samples')
    time_spent = models.DurationField(default=datetime.timedelta,
        help_text="Total recorded time to complete the campaign")
    is_frozen = models.BooleanField(default=False,
        help_text="When True, answers to that sample cannot be updated.")
    extra = get_extra_field_class()(null=True)

    def __str__(self):
        return str(self.slug)

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(uuid.uuid4().hex)
        return super(Sample, self).save(
            force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields)

    def get_answers_by_rank(self):
        # We attempt to get Django ORM to generate SQL equivalent to:
        # ```
        # SELECT survey_answer.* FROM survey_answer
        # INNER JOIN survey_sample
        # ON survey_answer.sample_id = survey_sample.id
        # INNER JOIN survey_enumeratedquestions
        # ON survey_answer.question_id = survey_enumeratedquestions.question_id
        # ON survey_sample.campaign_id = survey_enumeratedquestions.campaign_id
        # WHERE survey_answer.sample_id = %(sample_id)d
        # ORDER BY survey_enumeratedquestions.rank
        # ```
        queryset = Answer.objects.filter(
            sample=self,
            question__campaigns__in=[self.campaign.pk]).order_by(
            'question__enumeratedquestions__rank').annotate(
                rank=models.F('question__enumeratedquestions__rank'))
        return queryset


class AnswerManager(models.Manager):

    def populate(self, sample):
        """
        Return a list of ``Answer`` for all questions in the campaign
        associated to a *sample* even when there are no such record
        in the db.
        """
        answers = self.filter(sample=sample)
        if sample.campaign:
            questions = get_question_model().objects.filter(
                campaigns__pk=sample.campaign.pk).exclude(
                pk__in=answers.values('question'))
            answers = list(answers)
            for question in questions:
                answers += [Answer(question=question, sample=sample)]
        return answers


@python_2_unicode_compatible
class Answer(models.Model):
    """
    An Answer to a Question as part of Sample to a Campaign.
    """
    objects = AnswerManager()

    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(settings.QUESTION_MODEL,
        on_delete=models.PROTECT)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    measured = models.IntegerField(null=True)
    denominator = models.IntegerField(null=True, default=1)
    collected_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, on_delete=models.PROTECT)
    # XXX Optional fields when the answer is part of a campaign.
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE,
        related_name='answers')

    class Meta:
        unique_together = ('sample', 'question', 'metric')

    def __str__(self):
        return '%s-%d' % (self.sample.slug, self.question.slug)

    @property
    def as_text_value(self):
        if self.unit.system in Unit.NUMERICAL_SYSTEMS:
            return self.measured
        return Choice.objects.get(pk=self.measured).text

    def get_multiple_choices(self):
        text = Choice.objects.get(pk=self.measured).text
        return text.replace('[', '').replace(']', '').replace(
            'u\'', '').replace('\'', '').split(', ')


@python_2_unicode_compatible
class EditableFilter(SlugTitleMixin, models.Model):
    """
    A model type and list of predicates to create a subset of the
    of the rows of a model type
    """

    slug = models.SlugField(unique=True,
        help_text="Unique identifier for the sample. It can be used in a URL.")
    title = models.CharField(max_length=255,
        help_text="Title for the filter")
    tags = models.CharField(max_length=255,
        help_text="Helpful tags")

    def __str__(self):
        return str(self.slug)

    def as_kwargs(self):
        includes = {}
        excludes = {}
        for predicate in self.predicates.all().order_by('rank'):
            if predicate.selector == 'keepmatching':
                includes.update(predicate.as_kwargs())
            elif predicate.selector == 'removematching':
                excludes.update(predicate.as_kwargs())
        return includes, excludes


@python_2_unicode_compatible
class EditablePredicate(models.Model):
    """
    A predicate describing a step to narrow or enlarge
    a set of records in a portfolio.
    """
    rank = models.IntegerField()
    editable_filter = models.ForeignKey(
        EditableFilter, on_delete=models.CASCADE, related_name='predicates')
    operator = models.CharField(max_length=255)
    operand = models.CharField(max_length=255)
    field = models.CharField(max_length=255) # field on a Question.
    selector = models.CharField(max_length=255)

    def __str__(self):
        return '%s-%d' % (self.portfolio.slug, int(self.rank))

    def as_kwargs(self):
        kwargs = {}
        if self.operator == 'equals':
            kwargs = {self.field: self.operand}
        elif self.operator == 'startsWith':
            kwargs = {"%s__startswith" % self.field: self.operand}
        elif self.operator == 'endsWith':
            kwargs = {"%s__endswith" % self.field: self.operand}
        elif self.operator == 'contains':
            kwargs = {"%s__contains" % self.field: self.operand}
        return kwargs


@python_2_unicode_compatible
class Matrix(SlugTitleMixin, models.Model):
    """
    Represent a set of cohorts against a metric.
    """

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True,
        help_text=_("Long form description of the matrix"))
    account = models.ForeignKey(settings.BELONGS_MODEL,
        null=True, on_delete=models.CASCADE)
    metric = models.ForeignKey(EditableFilter, related_name='measured',
        null=True, on_delete=models.PROTECT)
    cohorts = models.ManyToManyField(EditableFilter, related_name='matrices')
    cut = models.ForeignKey(EditableFilter,
        null=True, on_delete=models.SET_NULL, related_name='cuts')
    extra = get_extra_field_class()(null=True)

    def __str__(self):
        return str(self.slug)
