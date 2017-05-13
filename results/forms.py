from django import forms
from .models import Result, CGPA
from .fields import RestrictedFileField

class BatchResultForm(forms.ModelForm):

    class Meta:
        model = Result
        exclude = ('semester', 'course', 'date_created', 'session', 'level', 'course_load', 'credit_load')
        
class ResultForm(forms.ModelForm):
    
    class Meta:
        model = Result
        exclude = ('date_created', 'course_load', 'credit_load')
        

    
class CGPAForm(forms.ModelForm):
    
    class Meta:
        model = CGPA
        exclude = ('cgpa','date_created')
        
class ResultImportForm(forms.Form):
    # File size limited to 2MB
    file = RestrictedFileField(
        label='CSV File (Max Size 2MB)',
        content_types=[
            'application/binary',
            'application/csv',
            'application/octet-stream',
            'application/vnd.ms-excel',
            'text/csv',
            'text/plain',
        ],
        max_upload_size=2097152,
    )