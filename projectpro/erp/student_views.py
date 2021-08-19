from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
import datetime

from django.views.decorators.csrf import csrf_exempt

from erp.models import Notes, Notice, CustomUser, Student, Mark, Subject, Attendance, AttendanceSave, Course, SessionYearModel

def student_home(request):
    student_obj=Student.objects.get(admin=request.user.id)
    attendance_total=AttendanceSave.objects.filter(students_id=student_obj).count()
    attendance_present=AttendanceSave.objects.filter(students_id=student_obj,status=True).count()
    attendance_absent=AttendanceSave.objects.filter(students_id=student_obj,status=False).count()
    course=Course.objects.get(id=student_obj.course_id.id)
    subjects=Subject.objects.filter(course_id=course).count()
    #subjects_data=Subject.objects.filter(course_id=course)
    #session_obj=SessionYearModel.object.get(id=student_obj.session_year_id.id)
    #class_room=OnlineClassRoom.objects.filter(subject__in=subjects_data,is_active=True,session_years=session_obj)

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subject.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance=Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count=AttendanceSave.objects.filter(attendance_id__in=attendance,status=True,students_id=student_obj.id).count()
        attendance_absent_count=AttendanceSave.objects.filter(attendance_id__in=attendance,status=False,students_id=student_obj.id).count()
        subject_name.append(subject.sub_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"student_template/student_home_template.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subject":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent})


def show_notes(request):
    notes = Notes.objects.all()
    return render(request, "student_template/show_notes_template.html", {"notes": notes})

def show_notice(request):
    notice = Notice.objects.all()
    return render(request, "student_template/show_notice_template.html", {"notice": notice})

def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Student.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        password=request.POST.get("password")
        address=request.POST.get("address")
        mobile = request.POST.get("mobile")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            student=Student.objects.get(admin=customuser)
            student.address=address
            student.mob_no = mobile
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))

def student_view_result(request):
    student=Student.objects.get(admin=request.user.id)
    mark=Mark.objects.filter(student_id=student.id)
    return render(request,"student_template/student_result.html",{"mark":mark})

def student_view_attendance(request):
    student=Student.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subject.objects.filter(course_id=course)
    return render(request,"student_template/student_view_attendance.html",{"subject":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subject.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Student.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceSave.objects.filter(attendance_id__in=attendance,students_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

@csrf_exempt
def student_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        student=Student.objects.get(admin=request.user.id)
        student.fcm_token=token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")