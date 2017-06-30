from django.contrib import admin
from students.models import *

class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__','reg_number','level','department', 'year_of_graduation', 'clearance_status', 'make_decision')

    def get_list_display(self, request):
    	self.user = request.user
    	return super(StudentAdmin, self).get_list_display(request)

    def make_decision(self, obj):
    	print(dir(obj))
    	content=""
    	for proceeding in obj.get_available_proceedings(self.user):
    		content += "<button value='' class='btn btn-primary btn-sm' style='margin: 2px;'>%s</button>" % (proceeding.meta.transition)
    	return content

    make_decision.allow_tags = True

admin.site.register(Student, StudentAdmin)
admin.site.register(Document)
admin.site.register(Project)
admin.site.register(Scholarship)

# Register your models here.
