from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from .models import Student
from .forms import *
from django.utils.decorators import method_decorator
from institutions.models import Department, Faculty
from results.models import Result
from results.forms import ImportForm
from students.models import *
from students.forms import StudentCreationForm
from result_analytics.utils.excel import ExcelReport
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.db import transaction
from django.contrib import messages
from .utils import user_is_student, generate_mapper_excel
from django.utils.decorators import method_decorator
from courses.models import Course
from analyzer.utils import StudentChartData, cgpaData
from notifications.signals import notify
from utils.url_dispatcher import get_url
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from results.utils import Computation as cp
from .utils import import_student_from_csv
try:
    import json
except:
    import simplejson as json


class StudentListView(ListView):
    model = Student
    template_name = 'students/_list_students.html'
    paginated_by = settings.PAGE_SIZE

    def get_queryset(self):
        queryset = Student.objects.filter(institution_id=self.request.user.lecturer.institution.id)
        print(queryset)
        department = self.request.GET.get("department", "all")
        faculty = self.request.GET.get("faculty", "all")
        student = self.request.GET.get("student", "")
        level = self.request.GET.get("level", "all")
        status = self.request.GET.get("status", "status")

        if department != "all":
            queryset = queryset.filter(department__name=department)
        if faculty != "all":
            queryset = queryset.filter(faculty__name=faculty)
        if student != "":
            queryset = queryset.filter(Q(reg_number__icontains=student) | Q(last_name__icontains=student) | Q(first_name__icontains=student))
        if level != "all":
            queryset = queryset.filter(level=level)
        if status != "status":
            queryset = queryset.filter(user_status=status)
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StudentListView, self).get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        context["faculties"] = Faculty.objects.all()
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginated_by)
        page = self.request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        context['students'] = queryset
        return context

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.lecturer.is_admin))
    def dispatch(self, request, *args, **kwargs):
        return super(StudentListView, self).dispatch(request, *args, **kwargs)

@login_required
@user_passes_test(lambda u: u.lecturer.is_admin)
def create_student(request):
    if request.method == "POST":
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            try:
                new_student = form.save(commit=False)
                new_student.institution = request.user.lecturer.institution
                new_student.save()
                messages.success(request, "%s's record has been successfully created." % (new_student))
                return HttpResponseRedirect(reverse('students:student_account', kwargs={'student_slug': new_student.slug}))
            except Exception as e:
                messages.error(request, e)
    else:
        form = StudentCreationForm()
    return render(request, 'students/new_student.html', {'form': list(form)})


@login_required
def student_profile(request, student_slug):
    template_name = ''

    student = get_object_or_404(Student, slug=student_slug)
    is_own_profile = (student.user == request.user)
    if is_own_profile:
        template_name = 'accounts'
    else:
        template_name = 'student_profile'

    context = {'student': student}
    context['my_rank'] = ranking(student)
    context['documents'] = Document.objects.filter(student=student)
    context['scholarships'] = Scholarship.objects.filter(student=student)


    documents = student.document_set.all()

    return render(request, 'students/%s.html' % (template_name), context)


def ranking(student):
    results = Result.objects.all()
    ranking_data = {}

    all_students = Student.objects.all()
    for stu in all_students:
        grade = 0
        for result in results:
            if result.student == stu:
                grade+=result.credit_load
        ranking_data[stu] = grade
    sort = sorted(ranking_data, key= ranking_data.__getitem__, reverse=True)

    return sort.index(student)+1

def export_excel(request):
    students = ((e.last_name, e.first_name, e.reg_number, e.level, e.sex, e.birth_date or '', e.program_type, e.department.name or '', e.faculty.name or '')
        for e in Student.objects.filter(institution=request.user.lecturer.institution).order_by('level'))
    fields = ["last_name", "first_name", "reg_number", "level", "sex", "birth_date", "program_type", "department", "faculty"]
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment;filename=students.xls"
    report = ExcelReport(students, fields, groupby=request.GET.get('groupby'))
    report.write(response)
    return response

@user_passes_test(user_is_student, login_url='/login/')
@login_required
def accounts(request):
    return render(request, 'students/accounts.html', {})
# Create your views here.

def update_photo(request):
    student = get_object_or_404(Student, pk=request.user.student.id)
    if request.method == "POST":
        photo = request.FILES['photo']

        student.photo = photo
        student.save()
    return HttpResponseRedirect(reverse('students:student_account', kwargs={'student_slug': student.slug}))


@login_required
@user_passes_test(lambda u:u.lecturer.is_admin, login_url="/login/")
def mapper_excel_generator(request):
    form = ImportForm()
    return render_to_response('students/generate_mapper.html', {'form': form}, context_instance=RequestContext(request),)


@login_required
@user_passes_test(lambda u:u.lecturer.is_admin, login_url="/login/")
def generate(request):
    if request.method == 'POST':
        try:
            # import pdb
            # pdb.set_trace()
            excel_file = request.FILES['file']
            print(excel_file.size)
            if excel_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (excel_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("students:mapper"))
            response = generate_mapper_excel(excel_file)
            return response
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('students:mapper'))


class StudentAnalyticsView(TemplateView):
    template_name = 'students/_analysis.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAnalyticsView, self).get_context_data(**kwargs)
        if Result.objects.filter(student=self.request.user.student).exists():
            context['fcgpa'] = cgpaData.get_fcgpa(self.request.user.student.id)
            context['exam_no'] = Result.objects.filter(student_id=self.request.user.student.id).count()
            context['avg_score'] = "%.2f" % (Result.objects.filter(student_id=self.request.user.student.id).values('total_score')\
                                    .aggregate(avg=Avg('total_score'))['avg'])
            context['high_score'] = Result.objects.filter(student_id=self.request.user.student.id).order_by('-total_score')[0]
        else:
            context['fcgpa'] = max(cp.get_grades(self.request.user.student.institution))
            context['avg_score'] = float(0)
        return context

    @method_decorator(user_passes_test(user_is_student))
    def dispatch(self,request, *args, **kwargs):
        return super(StudentAnalyticsView, self).dispatch(request, *args, **kwargs)


def student_chart_json(request):
    data = {}
    params = request.GET
    level = params.get('level')
    data = StudentChartData.student_result_data(request.user.student.id, level)
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def generate_mapper_json(request):
    map_code = ""
    message = ""
    if request.method == 'GET':
        params = request.GET
        short_code = params.get('short_code')
        reg_number = params.get('reg_number')

        if short_code != "" and reg_number != "":
            if UniqueMapper.objects.filter(reg_number=reg_number, short_institution_name=short_code).exists():
                message = "You already have a mapper"
                map_code = UniqueMapper.objects.filter(reg_number=reg_number, short_institution_name=short_code)[0].unique_map
            else:
                mapper = UniqueMapper(reg_number=reg_number, short_institution_name=short_code)
                mapper.save()
                map_code = mapper.unique_map
                message = "Successfully creates a map code"
    data = {
        "map_code": map_code,
        "message": message,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def edit_profile(request):
    context ={}
    student = Student.objects.get(user=request.user)
    template_name = 'students/_edit_profile.html'
    if request.method == 'POST':
        inst_form = SchoolForm(request.POST, request.FILES, instance=student)
        b_form = BasicProfileForm(request.POST, request.FILES, instance=student)
        p_form = PersonalInformationForm(request.POST, request.FILES, instance=student)
        if inst_form.is_valid() and b_form.is_valid() and p_form.is_valid():
            try:
                b_form.save()
                messages.success(request, "Your profile was successfully updated")
                return HttpResponseRedirect(reverse('students:student_account', kwargs={'student_slug':student.slug}))
            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('students:edit-profile'))
    else:
        inst_form = SchoolForm(instance=student)
        p_form = PersonalInformationForm(instance=student)
        b_form = BasicProfileForm(instance=student)
        context = {
            'inst_form': inst_form,
            'p_form': p_form,
            'b_form': b_form,
            'student': student
        }
    return render(request, template_name, context)

@login_required
def request_help(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    own = request.user.student
    notify.send(request.user, recipient=student.user,
        description=\
        get_url(request, reverse('students:student_account', kwargs={'student_slug':own.slug})),
        verb="%s is requesting for your help. Can you assist?" % (request.user.student))
    messages.success(request, "Your request has been sent to %s.\
     He will get back to you soon" % (student))
    print(":Done")
    return HttpResponseRedirect(reverse('dashboard'))


@login_required
@user_passes_test(lambda u: u.lecturer.is_admin, login_url="/login/")
def import_student_data(request):
    form = ImportForm()
    template_name = 'students/student_import.html'
    return render(request, template_name, {'form': form})


@login_required
@user_passes_test(lambda u: u.lecturer.is_admin, login_url="/login/")
def upload_student_csv(request):
    if request.method == 'GET':
        return render(request, 'students/student_import.html', {})
    try:
        csv_file = request.FILES["file"]
        print(csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("students:student-import"))

        # If the file is too large
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("students:student-import"))

        # else continue
        posted, existed = import_student_from_csv(csv_file, request.user.lecturer)
        if posted > 0 and existed > 0:
            messages.success(request, "You successfully imported %s New records, but we found %s already existing ones" % (posted, existed))
        else:
            messages.info(request, "It appears you do not have any new records to import. Total Existing Records Found: %s" % (existed))
    except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse("students:students_list"))
