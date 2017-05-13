from django import forms
from django.core import validators
from django.forms import fields, widgets
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .widgets import SkillsWidget

class SkillsField(fields.Field):
    widget = SkillsWidget

    def __init__(self, queryset, required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        super(SkillsField, self).__init__(required, widget, label, initial, help_text, *args, **kwargs)
        self.queryset = queryset

    def prepare_value(self, value):
        if hasattr(value, '__iter__'):
            return u','.join(force_unicode(v) for v in value)
        return super(SkillsField, self).prepare_value(value)
    
    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return []
        skills = []
        for v in value.split(','):
            skills.append(force_unicode(v))
        return skills

    def clean(self, value):
        #import pdb; pdb.set_trace()
        if self.required and not value:
            raise forms.ValidationError(self.error_messages['required'])
        elif not self.required and not value:
            return []
        self.run_validators(value)
        pks = []
        for v in value.split(','):
            try:
                o = self.queryset.get(name__iexact=v)
            except self.queryset.model.DoesNotExist:
                # If this skill doesn't exist, create it.
                # Yeah, I know this is kinda messy, but we'll deal with cleanup later.
                # Or, more precisely, I'll let someone else worry about cleanup :-P
                o = self.queryset.create(name=v)
            pks.append(o.pk)
        qs = self.queryset.filter(pk__in=pks)
        return qs

