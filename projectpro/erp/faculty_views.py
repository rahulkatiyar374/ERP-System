import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from erp.models import Notice, Subject, Notes, SessionYearModel, Attendance, Student, CustomUser, Faculty, Department, \
    AttendanceSave, Mark, Course, LeaveReportStaff


def faculty_home(request):
    #For Fetch All Student Under Staff
    subjects=Subject.objects.filter(faculty_id=request.user.id)
    print("subject", subjects)
    course_id_list=[]
    for subject in subjects:
        course=Course.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    print("course_id_list is",course_id_list)
    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    print("final_course",final_course)

    department_id_list = []
    for department_id in course_id_list:
        if department_id not in department_id_list:
            department_id_list.append(department_id)
    print("department_id_list",department_id_list)

    students_count=Student.objects.filter(course_id__in=final_course, department_id__in=department_id_list).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #Fetch All Approve Leave
    #staff=Faculty.objects.get(admin=request.user.id)
    #leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    #Fetch Attendance Data by Subject
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.sub_name)
        attendance_list.append(attendance_count1)

    students_attendance=Student.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceSave.objects.filter(status=True,students_id=student.id).count()
        attendance_absent_count=AttendanceSave.objects.filter(status=False,students_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request,"faculty_template/home_content.html",{"student_count":students_count,"attendance_count":attendance_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})


def add_staff_notice(request):
    return render(request, "faculty_template/add_notice_template.html")

def add_staff_notice_save(request):
    if request.method!="POST":
        return HttpResponse("method is not allowed")
    else:
        message = request.POST.get("message")
        print(message)
        notice_file = request.FILES['notice']
        fs = FileSystemStorage()
        filename = fs.save(notice_file.name, notice_file)
        notice_file_url = fs.url(filename)
        try:
            notice_model = Notice(detail=message, file=notice_file_url)
            notice_model.save()
            messages.success(request, "Successfully add notice")
            return HttpResponseRedirect("/add_staff_notice")
        except:
            messages.error(request, "failed to add notice")
            return HttpResponseRedirect("/add_staff_notice")

def add_notes(request):
    subject = Subject.objects.all()
    return render(request, "faculty_template/add_notes_template.html", {"subject":subject})

def add_notes_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        subject_id = request.POST.get("subject")
        subject = Subject.objects.get(id=subject_id)
        print(subject)
        notes = request.POST.get("message")
        notes_file = request.FILES['notice']
        fs = FileSystemStorage()
        filename = fs.save(notes_file.name, notes_file)
        notes_file_url = fs.url(filename)
        try:
            notes = Notes(subject_id=subject, detail=notes, notes=notes_file_url)
            notes.save()
            messages.success(request, "Successfully add notes")
            return HttpResponseRedirect("/add_notes")
        except:
            messages.error(request, "failed to add notes")
            return HttpResponseRedirect("/add_notes")

def manage_notes(request):
    notes = Notes.objects.all()
    return render(request, "faculty_template/manage_notes_template.html", {"notes": notes})

def delete_notes(request, id):
    notes = Notes.objects.get(id=id)
    notes.delete()
    return HttpResponseRedirect("/manage_notes")

#def get_student(request,id):
#    attendance = get_object_or_404(Attendance, id=id)
#    student = Student.objects.filter(sessionyear_id=id)
#    return render(request, "faculty_template/get_student.html", {"attendance": attendance, "student": student})

def show_subject(request):
    subjects=Subject.objects.filter(faculty_id_id=request.user.id)
    print("show_subject::subject", subjects)
    session_years=SessionYearModel.object.all()
    department = Department.objects.all()
    print("department::",department)
    return render(request,"faculty_template/faculty_take_attendance.html",{"subject":subjects,"session_years":session_years ,"department":department})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    print("subject_id=", subject_id)
    session_year=request.POST.get("session_year")
    print("session year=",session_year)
    department_id = request.POST.get("department")
    print(department_id)

    subject=Subject.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year)
    department = Department.objects.get(id=department_id)
    students=Student.objects.filter(sessionyear_id=session_model, course_id=subject.course_id, department_id=department)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name, "rollnum":student.roll_no}
        list_data.append(data_small)
        print("student json list",list_data)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subject.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,date=attendance_date,sessionyear_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Student.objects.get(admin=stud['id'])
             attendance_report=AttendanceSave(students_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")




def staff_apply_leave(request):
    staff_obj = Faculty.objects.get(admin=request.user.id)
    leave_data=LeaveReportStaff.objects.filter(faculty_id=staff_obj)
    return render(request,"faculty_template/apply_leave.html",{"leave_data":leave_data})

def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        staff_obj=Faculty.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStaff(faculty_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))




def faculty_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    faculty=Faculty.objects.get(admin=user)
    return render(request,"faculty_template/faculty_profile.html",{"user":user,"faculty":faculty})

def faculty_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("faculty_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        mobile=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            faculty=Faculty.objects.get(admin=customuser.id)
            faculty.mob_no=mobile
            faculty.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("faculty_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("faculty_profile"))


def faculty_add_mark(request):
    subject=Subject.objects.filter(faculty_id=request.user.id)
    session_years= SessionYearModel.object.all()
    department = Department.objects.all()
    return render(request,"faculty_template/mark.html",{"subject":subject, "session_years":session_years, "department":department})

def save_student_mark(request):
    if request.method!='POST':
        return HttpResponseRedirect('staff_add_result')
    student_admin_id=request.POST.get('student_list')
    sessional1_marks=request.POST.get('sessional')
    sessional2_marks=request.POST.get('sessionaltwo')
    ta_mark = request.POST.get('ta')
    mock_mark = request.POST.get('mock')
    subject_id=request.POST.get('subject')
    department_id=request.POST.get('department')


    student_obj=Student.objects.get(admin=student_admin_id)
    subject_obj=Subject.objects.get(id=subject_id)
    department_obj = Department.objects.get(id=department_id)

    try:
        check_exist=Mark.objects.filter(subject_id=subject_obj,student_id=student_obj, department_id=department_obj).exists()
        if check_exist:
            result=Mark.objects.get(subject_id=subject_obj,student_id=student_obj, department_id=department_obj)
            result.sessional_1=sessional1_marks
            result.sessional_2=sessional2_marks
            result.ta = ta_mark
            result.mock = mock_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("faculty_add_mark"))
        else:
            result=Mark(student_id=student_obj,subject_id=subject_obj, department_id=department_obj, sessional_1=sessional1_marks,sessional_2=sessional2_marks, ta=ta_mark, mock=mock_mark)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("faculty_add_mark"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("faculty_add_mark"))

@csrf_exempt
def fetch_result_student(request):
    subject_id=request.POST.get('subject_id')
    print("fetch result subject_id",subject_id)
    student_id=request.POST.get('student_id')
    print("fetch result student_id", student_id)
    department_id = request.POST.get('department_id')
    print("fetch result department_id", department_id)
    student_obj=Student.objects.get(admin=student_id)
    result=Mark.objects.filter(student_id=student_obj.id,subject_id=subject_id, department_id=department_id).exists()
    if result:
        result=Mark.objects.get(student_id=student_obj.id,subject_id=subject_id, department_id=department_id)
        result_data={"sessional":result.sessional_1,"sessionaltwo":result.sessional_2, "ta":result.ta, "mock":result.mock}
        print("dugufg",result_data)
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Faculty.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def show(request):
    subject = Subject.objects.filter(faculty_id=request.user.id)
    course = Course.objects.all()
    department = Department.objects.all()
    return render(request, "faculty_template/show_subject.html",{"subject":subject, "department":department})
def student(request,id):
    student = Student.objects.filter(department_id=id)
    return render(request, "faculty_template/get_student.html", {"student":student})