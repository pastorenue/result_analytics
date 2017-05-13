from haystack import indexes
from employees.models import Employee
from easy_thumbnails.files import get_thumbnailer

class EmployeeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    position = indexes.CharField(model_attr='position__name')
    unit = indexes.CharField(model_attr='unit__name')
    location = indexes.CharField(model_attr='location__name')
    birth_date = indexes.DateField(model_attr='birth_date', null=True)
    hire_date = indexes.DateField(model_attr='hire_date')
    confirmation_date = indexes.DateField(model_attr='confirmation_date', null=True)
    termination_date = indexes.DateField(model_attr='termination_date', null=True)
    skills = indexes.MultiValueField()
    status = indexes.CharField(model_attr='status')
    name = indexes.CharField(model_attr='full_name', indexed=False)
    name_auto = indexes.EdgeNgramField(model_attr='full_name')
    email = indexes.CharField(model_attr='email', indexed=False)
    phone = indexes.CharField(model_attr='phone', indexed=False)
    photo = indexes.CharField(indexed=False)
    absolute_url = indexes.CharField(indexed=False)
    
    def get_model(self):
        return Employee
    
    def prepare_skills(self, obj):
        return list(obj.skills.values_list('skill__name', flat=True))

    def prepare_status(self, obj):
        return obj.get_status_display()

    def prepare_photo(self, obj):
        if obj.photo:
            # Return the path to the search thumbnail version of the employee's photo:
            return get_thumbnailer(obj.photo).get_thumbnail({'size': (125, 125), 'autocrop': True, 'crop': True}).url
        return ''

    def prepare_absolute_url(self, obj):
        return obj.get_absolute_url()

