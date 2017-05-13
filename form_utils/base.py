from django import forms
from django.conf import settings
from django.forms.models import construct_instance
from changerequest.models import ChangeTrackingModel

DEFAULT_FORM_JS = getattr(settings, 'DEFAULT_FORM_JS', ())
DEFAULT_FORM_CSS = getattr(settings, 'DEFAULT_FORM_CSS', {})

class MediaMixin(object):
    """Mix-in used to add default form media."""
    
    @property
    def media(self):
        media = forms.Media(
            extend=True,
            css=DEFAULT_FORM_CSS,
            js=DEFAULT_FORM_JS
        )
        for fld_name in self.fields:
            media += self.fields[fld_name].widget.media
        return media

class Form(MediaMixin, forms.Form):
    """Form base class, which automatically adds the default form media."""
    
    
def save_instance(form, instance, fields=None, fail_message='saved',
                  commit=True, exclude=None, construct=True):
    """
    Saves bound Form ``form``'s cleaned_data into model instance ``instance``.

    If commit=True, then the changes to ``instance`` will be saved to the
    database. Returns ``instance``.

    If construct=False, assume ``instance`` has already been constructed and
    just needs to be saved.
    """
    if construct:
        instance = construct_instance(form, instance, fields, exclude)
    opts = instance._meta
    if form.errors:
        raise ValueError("The %s could not be %s because the data didn't"
                         " validate." % (opts.object_name, fail_message))

    # Wrap up the saving of m2m data as a function.
    def save_m2m():
        cleaned_data = form.cleaned_data
        for f in opts.many_to_many:
            if fields and f.name not in fields:
                continue
            if f.name in cleaned_data:
                f.save_form_data(instance, cleaned_data[f.name])
    if commit:
        # If we are committing, save the instance and the m2m data immediately.
        instance.save()
        save_m2m()
    else:
        # We're not committing. Add a method to the form to allow deferred
        # saving of m2m data.
        form.save_m2m = save_m2m
    return instance

class ModelForm(MediaMixin, forms.ModelForm):
    """ModelForm base class, which automatically adds the default form media."""
    
    def save(self, commit=True):
        """
        Saves this ``form``'s cleaned_data into model instance
        ``self.instance``.

        If commit=True, then the changes to ``instance`` will be saved to the
        database. Returns ``instance``.
        """
        if self.instance.pk is None:
            fail_message = 'created'
        else:
            fail_message = 'changed'
        return save_instance(self, self.instance, self._meta.fields,
                             fail_message, commit, construct=False)

    save.alters_data = True
    