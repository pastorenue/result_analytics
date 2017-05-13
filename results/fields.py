"""
Source: http://chriskief.com/2013/10/19/limiting-upload-file-size-with-django-forms/
"""

from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = 2097152
        self.upload_to = kwargs.pop('upload_to', None)
        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        _('File size must be under %s. Current file size is %s.') \
                        % (filesizeformat(self.max_upload_size),
                           filesizeformat(data.size)))
            else:
                raise forms.ValidationError(
                    _('File type (%s) is not supported.') % data.content_type)
        except AttributeError:
            pass

        return data