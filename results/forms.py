from django import forms
from .models import Result, CGPA, Grading
from .fields import RestrictedFileField

class BatchResultForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(BatchResultForm, self).__init__(*args, **kwargs)
        self.fields['semester'].widget.attrs = {'placeholder' : _(u'Full name'), 'class': 'form-control', 'style': 'height: 19px;'}
        self.fields['course'].widget.attrs = {'placeholder' : _(u'Email'), 'class': 'form-control'}
        self.fields['session'].widget.attrs = {'placeholder' : _(u'Subject'), 'class': 'form-control'}
        self.fields['course_load'].widget.attrs = {'placeholder' : _(u'Phone'), 'class': 'form-control'}
        self.fields['level'].widget.attrs = {'placeholder' : _(u'Message'), 'class': 'form-control', 'rows': '10'}
        self.fields['credit_load'].widget.attrs = {'placeholder' : _(u'Message'), 'class': 'form-control', 'rows': '10'}

    class Meta:
        model = Result
        exclude = ('semester', 'course', 'date_created', 'session', 'level', 'course_load', 'credit_load')
        
class ResultForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(BatchResultForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs = {'placeholder' : _(u'Full name'), 'class': 'form-control', 'style': 'height: 19px;'}
        self.fields['course'].widget.attrs = {'placeholder' : _(u'Email'), 'class': 'form-control'}
        self.fields['session'].widget.attrs = {'placeholder' : _(u'Subject'), 'class': 'form-control'}
        self.fields['level'].widget.attrs = {'placeholder' : _(u'Message'), 'class': 'form-control', 'rows': '10'}
       
    class Meta:
        model = Result
        exclude = ('date_created', 'course_load', 'credit_load', 'department')
        

    
class ImportForm(forms.Form):
    # File size limited to 2MB
    file = RestrictedFileField(
        label='Upload File (Max Size 2MB)',
        content_types=[
            'application/binary',
            'application/ms-excel',
            'application/csv',
            'application/octet-stream',
            'application/vnd.ms-excel',
            'text/csv',
            'text/plain',
        ],
        max_upload_size=2097152,
    )


class BatchGradingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BatchGradingForm, self).__init__(*args, **kwargs)
        self.fields['caption'].widget.attrs = {'class': 'form-control input-sm', 'placeholder': 'Grade Letter'}
        self.fields['grade_points'].widget.attrs = {'class': 'form-control input-sm', 'placeholder': 'Grade Point'}
        self.fields['start'].widget.attrs = {'class': 'form-control input-sm'}
        self.fields['end'].widget.attrs = {'class': 'form-control input-sm'}

    class Meta:
        model = Grading
        exclude = ('institution',)


class GradingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GradingForm, self).__init__(*args, **kwargs)
        self.fields['institution'].widget.attrs = {'class': 'form-control input-sm'}

    class Meta:
        model = Grading
        fields = ('institution',)
