from django import forms
from django.forms import fields, widgets
from django.forms.util import flatatt
from django.utils import datetime_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from datetime import date
from json import dumps
from random import Random
import re

wmd_suffix_gen = Random()

DATE_FMT_RE = re.compile(r'(%[a-zA-Z]|%%|[^%]+)')
DATE_FMT_MAP = {
    '%a': 'ddd',
    '%A': 'dddd',
    '%d': 'dd',
    '%b': 'mmm',
    '%B': 'mmmm',
    '%m': 'mm',
    '%y': 'yy',
    '%Y': 'yyyy',
}

def py_to_js_dateformat(fmt):
    """Converts a Python datetime format to the Javascript format expected by our calendar widget."""
    bits = []
    for bit in DATE_FMT_RE.findall(fmt):
        bits.append(DATE_FMT_MAP.get(bit, bit))
    return ''.join(bits)

class CalendarWidget(widgets.TextInput):
    """A Calendar widget, which uses the jQuery Tools Calendar."""
    
    def __init__(self, attrs=None, **kwargs):
        super(CalendarWidget, self).__init__(attrs)
        self.attrs.update({'class': 'date-fld', 'autocomplete': 'off'})
        if 'format' in kwargs:
            try:
                self.format = kwargs['format']
            except:
                raise Exception(u'Invalid arguments')
            self.attrs['data-date-format'] = py_to_js_dateformat(self.format)
        if 'offset' in kwargs:
            try:
                y_o, x_o = kwargs['offset']
            except:
                raise Exception(u'"offset" should be a tuple of (y offset, x offset).')
            self.attrs['data-date-offset-y'] = y_o
            self.attrs['data-date-offset-x'] = x_o
        if 'year_range' in kwargs:
            try:
                r_min, r_max = kwargs['year_range']
            except:
                raise Exception(u'"year_range" should be a tuple of (min year offset, max year offset).')
            self.attrs['data-date-year-min'] = r_min
            self.attrs['data-date-year-max'] = r_max
            self.attrs['data-date-selectors'] = 1

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif hasattr(value, 'strftime'):
            dt = datetime_safe.new_date(value)
            self.attrs['data-value'] = dt.strftime('%Y-%m-%d')
            value = dt.strftime(self.format)
        else:
            self.attrs['data-value'] = value
        return super(CalendarWidget, self).render(name, value, attrs)

class DateFieldMixin(object):
    """Form Helper: modify all date fields in the subclassing form to use the calendar widget."""
    
    def __init__(self, *args, **kwargs):
        super(DateFieldMixin, self).__init__(*args, **kwargs)
        for fld_name in self.fields:
            fld = self.fields[fld_name]
            if isinstance(fld, (fields.DateField, fields.DateTimeField,)):
                fld.input_formats = ('%d/%m/%Y',)
                fld.widget = CalendarWidget(attrs=fld.widget.attrs, format=fld.input_formats[0])
                
    
class MarkdownEditorWidget(widgets.Textarea):
    """A Markdown WYSIWYG editor (uses the PageDown project: `http://code.google.com/p/pagedown`)."""
    
    class Media:
        extend = True
        css = {
            'all': ('wmd/markdown.css',)
        }
        js = ('wmd/Markdown.Converter.js',
              'wmd/Markdown.Sanitizer.js',
              'wmd/Markdown.Editor.js',)
        
    def render(self, name, value, attrs=None):
        """Renders the HTML required by the PageDown editor."""
        if value is None: value = ''
        suffix = '-%d' % wmd_suffix_gen.randint(1, 65535)
        attrs['id'] = 'wmd-input%s' % suffix
        attrs['class'] = ('%s wmd-input' % attrs['class']) if 'class' in attrs else 'wmd-input'
        final_attrs = self.build_attrs(attrs, name=name)
        out = [u'<div class="wmd-panel">']
        out.append(u'<div id="wmd-button-bar%s"></div>' % suffix)
        out.append(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))
        out.append(u'<div id="wmd-preview%s" class="wmd-preview">' % suffix)
        out.append(u'</div>')
        out.append(u"""
<script type="text/javascript">
(function() {
    var converter = Markdown.getSanitizingConverter();
    var options = {}; // Keep for later.
    var editor = Markdown.Editor(converter, "%s", options);
    editor.run();
})();
</script>
""" % suffix)
        return mark_safe(u''.join(out))
    

class RatingFieldRenderer(widgets.RadioFieldRenderer):
    """Custom rendering for the RadioSelect so it works better with our javascript."""

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            if i == 0:
                # Hacky: Skip first (expected blank) option
                continue
            attrs = dict(self.attrs, title=choice[1])
            yield widgets.RadioInput(self.name, self.value, attrs, (choice[0], ''), i)

    def render(self):
        """Output a <p> enclosing this set of radio fields."""
        return mark_safe(u'<p class="vRatingField">%s</p>' % u'\n'.join([force_unicode(r) for r in self]))

class RatingWidget(widgets.RadioSelect):
    """A star-rating widget."""
    
    renderer = RatingFieldRenderer

    class Media:
        extend = True
        css = {
            'all': ('css/rating.css',)
        }
        js = ('js/jquery.rating.js',)
        

class SkillsWidget(widgets.TextInput):
    """A tag-style input widget, for entering skills."""
    
    class Media:
        extend = True
        css = {
            'all': ('css/tokeninput.css',)
        }
        js = ('js/jquery.tokeninput.js', 'js/skills-init.js',)
        
    def __init__(self, *args, **kwargs):
        super(SkillsWidget, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'vSkillsField'
        
    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        value = value or ''
        skills = [{'id': 0, 'name': force_unicode(v)} for v in value.split(',') if v]
        if skills:
            attrs['data-value'] = dumps(skills)
        return super(SkillsWidget, self).render(name, value, attrs)
        
