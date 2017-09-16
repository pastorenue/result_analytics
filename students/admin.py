from django.contrib import admin
from students.models import *

def proceed_button(obj, proceeding):
    return """
    <a href="%s"' 
        style="margin: 2px;
        padding: 5px 15px;
        font-size: 10px;
        width: 200px;
        text-align: center;
        border-radius: 16px;
        background: #2980b9;
        color: #fff;">%s</a>
        """ % ("", proceeding.meta.transition)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__','reg_number', 'level','department', 'year_of_graduation')

    def get_list_display(self, request):
    	self.user = request.user
    	return super(StudentAdmin, self).get_list_display(request)

    # def clearance_process(self, obj):
    # 	content=""
    # 	for proceeding in obj.get_available_proceedings(self.user):
    # 		content += proceed_button(obj, proceeding)
    # 	return content

    # clearance_process.allow_tags = True

class UniqueMapAdmin(admin.ModelAdmin):
    list_display = ('reg_number', 'unique_map')

admin.site.register(UniqueMapper, UniqueMapAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Document)
admin.site.register(Scholarship)

# Register your models here.
