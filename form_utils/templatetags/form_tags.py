from django import forms, template
from django.conf import settings
from django.forms import formsets
from django.forms.util import ErrorDict
from django.template import Library, Variable
from django.utils.safestring import mark_safe

register = Library()

@register.tag
def form_errors(parser, token):
    """Render a list of all non-field errors in the supplied Forms."""

    class _Node(template.Node):
        def __init__(self, extra_context):
            self._context = extra_context

        def render(self, context):
            form_list = []
            for f in [expr.resolve(context) for expr in self._context]:
                if isinstance(f, forms.BaseForm):
                    form_list.append(f)
                elif isinstance(f, formsets.BaseFormSet):
                    form_list.extend(f.forms)
                else:
                    raise TypeError('Arguments should be Form or FormSet instances.')

            non_field_errors, field_errors = [], []
            
            # First, get all non-field errors:
            for form in form_list:
                if '__all__' in form.errors:
                    non_field_errors.extend(form.errors['__all__'])
            # Next, get all field errors, preserving field order:
            for form in form_list:
                for fld in form:
                    if fld.errors:
                        field_errors.extend([
                            u'%s: %s' % (fld.label, err) for err in fld.errors
                        ])
            
            out = []
            if field_errors or non_field_errors:
                out.extend([u'<div class="message error">',
                            #u'<i class="fa fa-exclamation-circle fa-2x opacity-40 pull-left"></i>',
                            u'Please correct the errors in the form below'])
                if non_field_errors:
                    as_ul = u'<ul>%s</ul>' % ''.join([u'<li>%s</li>' % e for e in non_field_errors])
                    out.append(as_ul)
                out.append(u'</div>')
            return mark_safe(u'\n'.join(out))

    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError('%r requires at least one argument' % token.contents.split()[0])
    extra_context = [Variable(expr.strip()) for expr in args.split(',')]
    return _Node(extra_context)

def form_row(form, fld, start_tag, end_tag, show_help=True):
    has_errors = bool(fld.errors)
    widget = fld.field.widget
    fld_id = widget.id_for_label(widget.attrs.get('id') or fld.auto_id)
    fld_label = ((u'<strong class="required">%s</strong>' % fld.label if fld.field.required else fld.label) if fld.label else u'')
    if fld_label and fld.help_text and show_help:
        fld_label += u' <a href="#%s_help" class="show-tip" data-tip-position="center right" data-tip-offset-x="5">(?)</a>' % fld_id
    fld_errors = u'\n'.join([u'<span class="error">%s</span>' % err for err in fld.errors]) if has_errors else u''
    out = []

    li_attrs = []
    if fld.help_text and show_help: li_attrs.append(u'has-tip')
    if has_errors: li_attrs.append(u'has-errors')
    out.append(start_tag % ((u' class="%s"' % ' '.join(li_attrs)) if li_attrs else u''))
    if isinstance(fld.field, forms.BooleanField) and not isinstance(fld.field, forms.NullBooleanField):
        out.append(u'%s <label for="%s">%s %s</label>' % (fld_errors, fld_id, fld, fld_label))
    elif not fld_label:
        out.extend([fld_errors, unicode(fld)])
    else:
        is_radio = isinstance(fld.field.widget, forms.RadioSelect)
        out.append(u'<label%s>%s</label>%s %s' % ((u'' if is_radio else u' for="%s"' % fld_id), fld_label, fld_errors, fld))
    if fld.help_text and show_help:
        out.append(u'<em id="%s_help" class="tip-content">%s</em>' % (fld_id, fld.help_text))
    out.append(end_tag)

    out = u''.join(out)
    return out

@register.simple_tag
def render_form_row(form, field_name, start_tag=u'<li%s>\n', end_tag=u'</li>\n', show_help=True):
    """Renders a bound form field wrapped in a HTML element -- by default "<li>"."""
    fld = form[field_name]
    out = form_row(form, fld, start_tag, end_tag, show_help)
    return mark_safe(out)
    
@register.simple_tag(takes_context=True)
def render_csrf_token(context):
    """Renders a hidden field with the current CSRF token."""
    csrf_token = context.get('csrf_token', None)
    if csrf_token:
        if csrf_token != 'NOTPROVIDED':
            return mark_safe(u'<input type="hidden" name="csrfmiddlewaretoken" value="%s" />' % csrf_token)
    else:
        # Token might be missing because of misconfiguration, so we raise a warning:
        if settings.DEBUG:
            import warnings
            warnings.warn("A {% csrf_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.")

@register.simple_tag(takes_context=True)
def render_form(context, form, start_tag=u'<li%s>\n', end_tag=u'</li>\n', show_help=True):
    """Renders a bound form as a collection of HTML elements."""
    out = []
    for fld in form.visible_fields():
        out.append(form_row(form, fld, start_tag, end_tag, show_help))
    hidden_fields = form.hidden_fields()
    out.append(start_tag % ' style="display:none; visibility: hidden"')
    out.append(render_csrf_token(context))
    if hidden_fields:
        for fld in hidden_fields:
            out.append(unicode(fld))
    out.append(end_tag)
    out = u''.join(out)
    return mark_safe(out)
