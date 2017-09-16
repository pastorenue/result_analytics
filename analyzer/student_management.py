from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import ChartData, cgpaData
from students.models import Student
from students.utils import user_is_student


@user_passes_test(user_is_student)
@login_required
def all_analysis(student_id):
    #All cgpa analysis
    cgpa_data = cgpaData.get_cgpa()
   
    