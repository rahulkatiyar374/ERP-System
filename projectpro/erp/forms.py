from django import forms
from django.forms import ChoiceField

from erp.models import Course, Department, SessionYearModel, Subject


class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    roll_no=forms.IntegerField(label="Roll Number",widget=forms.NumberInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sex = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    father_name = forms.CharField(label="Father Name", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    mother_name = forms.CharField(label="Mother Name", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    mob_no=forms.IntegerField(label="Mobile Number",widget=forms.NumberInput(attrs={"class":"form-control"}))
    pmob_no=forms.IntegerField(label="Parent Mobile Number",widget=forms.NumberInput(attrs={"class":"form-control"}))



    courses=Course.objects.all()
    course_list=[]
    for course in courses:
        small_course=(course.id,course.c_name)
        course_list.append(small_course)

    departments = Department.objects.all()
    department_list = []
    for department in departments:
        small_department = (department.id, department.d_name)
        department_list.append(small_department)



    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    department = forms.ChoiceField(label="Department", choices=department_list,widget=forms.Select(attrs={"class": "form-control"}))
    sessions = SessionYearModel.object.all()
    session_list = []
    for ses in sessions:
        small_ses = (ses.id, str(ses.session_start_year) + "   TO  " + str(ses.session_end_year))
        session_list.append(small_ses)
    session_year_id=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    roll_no = forms.IntegerField(label="Roll Number", widget=forms.NumberInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sex = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    father_name = forms.CharField(label="Father Name", max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    mother_name = forms.CharField(label="Mother Name", max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    mob_no = forms.IntegerField(label="Mobile Number", widget=forms.NumberInput(attrs={"class": "form-control"}))
    pmob_no = forms.IntegerField(label="Parent Mobile Number",
                                 widget=forms.NumberInput(attrs={"class": "form-control"}))

    courses = Course.objects.all()
    course_list = []
    for course in courses:
        small_course = (course.id, course.c_name)
        course_list.append(small_course)

    departments = Department.objects.all()
    department_list = []
    for department in departments:
        small_department = (department.id, department.d_name)
        department_list.append(small_department)

    course = forms.ChoiceField(label="Course", choices=course_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    department = forms.ChoiceField(label="Department", choices=department_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year) + "   TO  " + str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list = []

    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class EditMarkForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.faculty_id=kwargs.pop("faculty_id")
        super(EditMarkForm,self).__init__(*args,**kwargs)
        subject_list=[]
        try:
            subjects=Subject.objects.filter(faculty_id=self.faculty_id)
            for subject in subjects:
                subject_single=(subject.id,subject.sub_name)
                subject_list.append(subject_single)
        except:
            subject_list=[]
        self.fields['subject_id'].choices=subject_list

    session_list=[]
    try:
        sessions=SessionYearModel.object.all()
        for session in sessions:
            session_single=(session.id,str(session.session_start_year)+" TO "+str(session.session_end_year))
            session_list.append(session_single)
    except:
        session_list=[]

    department_list = []
    try:
        department = Department.objects.all()
        for departments in department:
            department_single = (departments.id, departments.d_name)
            department_list.append(department_single)
    except:
        department_list = []

    subject_id=forms.ChoiceField(label="Subject",widget=forms.Select(attrs={"class":"form-control"}))
    department_id = forms.ChoiceField(label="Department", choices=department_list, widget=forms.Select(attrs={"class": "form-control"}))
    session_ids=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    student_ids=ChoiceNoValidation(label="Student",widget=forms.Select(attrs={"class":"form-control"}))
    sessional_marks=forms.CharField(label="First Sessional Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
    sessionaltwo_marks=forms.CharField(label="Second Sessional Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
    ta_marks=forms.CharField(label="TA Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
    mock_marks=forms.CharField(label="Mock Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
