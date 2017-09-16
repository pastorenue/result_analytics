from .models import *


class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'file',
            'tag',
        )
        
