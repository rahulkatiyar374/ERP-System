import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

#from erp.forms import AddStudentForm, EditStudentForm
from django.views.decorators.csrf import csrf_exempt

from erp.forms import AddStudentForm, EditStudentForm
from erp.models import CustomUser, Faculty, Course, Subject, Student, Department, Notice, SessionYearModel, Attendance, \
    AttendanceSave, LeaveReportStaff


def admin_home(request):
    student_count1=Student.objects.all().count()
    staff_count=Faculty.objects.all().count()
    subject_count=Subject.objects.all().count()
    course_count=Course.objects.all().count()

    course_all=Course.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subject.objects.filter(course_id=course.id).count()
        students=Student.objects.filter(course_id=course.id).count()
        course_name_list.append(course.c_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subject.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Course.objects.get(id=subject.course_id.id)
        student_count=Student.objects.filter(course_id=course.id).count()
        subject_list.append(subject.sub_name)
        student_count_list_in_subject.append(student_count)

    staffs=Faculty.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subject.objects.filter(faculty_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        #leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        #attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Student.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceSave.objects.filter(students_id=student.id,status=True).count()
        absent=AttendanceSave.objects.filter(students_id=student.id,status=False).count()
        #leaves=LeaveReport.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(absent)
        student_name_list.append(student.admin.username)


    return render(request,"admin_template/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})

def add_faculty(request):
    department = Department.objects.all()
    return render(request,"admin_template/add_faculty_template.html", {"department": department})

def add_faculty_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mob_no=request.POST.get("mobile")
        department_id = request.POST.get("department")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.faculty.mob_no = mob_no
            department_obj = Department.objects.get(id=department_id)
            user.faculty.department_id = department_obj
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect("add_faculty")
        except:
            messages.error(request,"Failed to Add Faculty")
            return HttpResponseRedirect("add_faculty")

def add_course(request):
    return render(request, "admin_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        course_duration = request.POST.get("course_duration")
        try:
            course_model = Course(c_name=course,c_duration=course_duration)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect("/add_course")

def add_department(request):
    cour = Course.objects.all()
    return render(request, "admin_template/add_department_template.html", {"course": cour})

def add_department_save(request):
    if request.method!="POST":
        return HttpResponse("Method is not allowed")
    else:
        department_name = request.POST.get("dpartmentname")
        course_id = request.POST.get("course")
        course = Course.objects.get(id=course_id)
    try:
        department_model = Department(course_id=course, d_name=department_name)
        department_model.save()
        messages.success(request, "Successfully Added Department")
        return HttpResponseRedirect("/add_department")
    except:
        messages.error(request, "Failed To Add Department")
        return HttpResponse("sorry department")

def add_subject(request):
    courses = Course.objects.all()
    facultys = CustomUser.objects.filter(user_type=2)
    return render(request, "admin_template/add_subject_template.html", {"course": courses,"faculty": facultys})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method is not allowed")
    else:
        subject = request.POST.get("subject_name")
        code = request.POST.get("subject_code")
        course_id = request.POST.get("course")
        course = Course.objects.get(id=course_id)
        faculty_id = request.POST.get("staff")
        faculty = CustomUser.objects.get(id=faculty_id)
    try:
        Subject_model = Subject(sub_code=code, sub_name=subject, course_id=course, faculty_id=faculty)
        Subject_model.save()
        messages.success(request, "Successfully Added Subject")
        return HttpResponseRedirect("/add_subject")
    except:
        messages.error(request, "Failed To Add Subject")
        return HttpResponse("/add_subject")


def add_notice(request):
    return render(request,"admin_template/add_notice_template.html")

def add_notice_save(request):
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
            return HttpResponseRedirect("/add_notice")
        except:
            messages.error(request, "failed to add notice")
            return HttpResponseRedirect("/add_notice")

def add_student(request):
    form=AddStudentForm()
    return render(request,"admin_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            mob_no = form.cleaned_data["mob_no"]
            pmob_no = form.cleaned_data["pmob_no"]
            father_name = form.cleaned_data["father_name"]
            mother_name = form.cleaned_data["mother_name"]
            roll_no = form.cleaned_data["roll_no"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            print(address)
            sessionyear_id=form.cleaned_data["session_year_id"]
            print(sessionyear_id)
            course_id=form.cleaned_data["course"]
            department_id=form.cleaned_data["department"]
            sex=form.cleaned_data["sex"]

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.student.address=address
                user.student.roll_no = roll_no
                user.student.mob_no = mob_no
                user.student.pmob_no = pmob_no
                user.student.fname = father_name
                user.student.mname = mother_name
                course_obj=Course.objects.get(id=course_id)
                user.student.course_id=course_obj
                department_obj = Department.objects.get(id=department_id)
                user.student.department_id = department_obj
                session_obj = SessionYearModel.object.get(id=sessionyear_id)
                user.student.sessionyear_id = session_obj
                user.student.gender=sex
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "admin_template/add_student_template.html", {"form": form})


def manage_faculty(request):
    faculty = Faculty.objects.all()
    return render(request, "admin_template/manage_faculty_template.html", {"faculty": faculty})

def manage_course(request):
    course = Course.objects.all()
    return render(request, "admin_template/manage_course_template.html", {"course": course})

def manage_notice(request):
    notice = Notice.objects.all()
    return render(request, "admin_template/manage_notice_template.html", {"notice": notice})

def manage_department(request):
    department = Department.objects.all()
    return render(request, "admin_template/manage_department_template.html", {"department": department})


def manage_student(request):
    student = Student.objects.all()
    return render(request, "admin_template/manage_student_template.html", {"student": student})

def manage_subject(request):
    subject = Subject.objects.all()
    return render(request, "admin_template/mannage_subject_template.html", {"subject": subject})

def edit_faculty(request, facultys_id):
    faculty = Faculty.objects.get(admin=facultys_id)
    department = Department.objects.all()
    return render(request, "admin_template/edit_faculty_template.html", {"faculty": faculty, "department": department})

def edit_faculty_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        faculty_id=request.POST.get("faculty_id")
        first_name=request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        email=request.POST.get("email")
        username=request.POST.get("username")
        mobile=request.POST.get("mobile")
        department_id = request.POST.get("department")

        try:
            user=CustomUser.objects.get(id=faculty_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            faculty_model=Faculty.objects.get(admin=faculty_id)
            department = Department.objects.get(id=department_id)
            faculty_model.department_id = department
            faculty_model.mob_no=mobile
            faculty_model.save()
            messages.success(request,"Successfully Edited Record")
            return HttpResponseRedirect("/edit_faculty/"+faculty_id)
        except:
            messages.error(request,"Failed to Edit Record")
            return HttpResponseRedirect("/edit_faculty/"+faculty_id)

def edit_course(request,courses_id):
    course = Course.objects.get(id=courses_id)
    return render(request, "admin_template/edit_course_template.html", {"course": course, "id": courses_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        courses_id = request.POST.get("courses_id")
        name = request.POST.get("course")
        duration = request.POST.get("course_duration")

        try:
            course_model=Course.objects.get(id=courses_id)
            course_model.c_name=name
            course_model.c_duration = duration
            course_model.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect("/edit_course/"+courses_id)
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect("/edit_course/"+courses_id)
def edit_department(request,departments_id):
    department = Department.objects.get(id=departments_id)
    course = Course.objects.all()
    return render(request, "admin_template/edit_department_template.html", {"department": department, "course": course})

def edit_department_save(request):
    if request.method!="POST":
        return HttpResponse("method is not allowed")
    else:
        department_id=request.POST.get("departments_id")
        name = request.POST.get("dpartmentname")
        course = request.POST.get("course")
        try:
            department_model = Department.objects.get(id=department_id)
            department_model.d_name = name
            courses = Course.objects.get(id=course)
            department_model.course_id = courses
            department_model.save()
            messages.success(request, "Successfully Edited Department")
            return HttpResponseRedirect("/edit_department/" +department_id)
        except:
            messages.error(request, "failed to Edit Department")
            return HttpResponseRedirect("/edit_department/" + department_id)

def edit_subject(request,subjects_id):
    subject = Subject.objects.get(id=subjects_id)
    course = Course.objects.all()
    faculty = CustomUser.objects.filter(user_type=2)
    return render(request, "admin_template/edit_subject_template.html", {"subject": subject, "course": course, "faculty": faculty})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("method is not allowed")
    else:
        subject_id = request.POST.get("subjects_id")
        print(subject_id)
        name = request.POST.get("subject_name")
        print(name)
        code = request.POST.get("subject_code")
        print(code)
        courses = request.POST.get("course")
        print("couses",courses)
       # facultys = request.POST.get("faculty")
       # print("faculty",facultys)
        try:
            subject_model = Subject.objects.get(id=subject_id)
            print(subject_model)
            subject_model.sub_name = name
            subject_model.sub_code = code
            course_obj = Course.objects.get(id=courses)
            subject_model.course_id = course_obj
            #faculty_obj = CustomUser.objects.get(id=facultys)
            #subject_model.faculty_id = faculty_obj
            subject_model.save()
            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect("/edit_subject/" + subject_id)
        except:
            messages.error(request, "failed to Edit Subject")
            return HttpResponseRedirect("/edit_subject/" + subject_id)
def edit_student(request,students_id):
    request.session['student_id']=students_id
    student=Student.objects.get(admin=students_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['mob_no'].initial = student.mob_no
    form.fields['roll_no'].initial = student.roll_no
    form.fields['pmob_no'].initial = student.pmob_no
    form.fields['father_name'].initial = student.fname
    form.fields['mother_name'].initial = student.mname
    form.fields['course'].initial=student.course_id.id
    form.fields['department'].initial = student.department_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.sessionyear_id.id
    return render(request,"admin_template/edit_student_template.html",{"form":form,"id":students_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        students_id=request.session.get("student_id")
        if students_id==None:
            return HttpResponseRedirect("manage_student")

        form=EditStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            mob_no = form.cleaned_data["mob_no"]
            pmob_no = form.cleaned_data["pmob_no"]
            father_name = form.cleaned_data["father_name"]
            mother_name = form.cleaned_data["mother_name"]
            roll_no = form.cleaned_data["roll_no"]
            address = form.cleaned_data["address"]
            sessionyear_id=form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            department_id = form.cleaned_data["department"]
            sex = form.cleaned_data["sex"]


            try:
                user=CustomUser.objects.get(id=students_id)
                user.first_name=first_name
                user.last_name=last_name
                user.email=email
                user.username=username
                user.save()
                student_model=Student.objects.get(admin=students_id)
                student_model.address=address
                student_model.mob_no=mob_no
                student_model.pmob_no=pmob_no
                student_model.fname=father_name
                student_model.mname=mother_name
                student_model.roll_no=roll_no
                session_obj = SessionYearModel.object.get(id=sessionyear_id)
                user.student.sessionyear_id = session_obj
                student_model.gender=sex
                course=Course.objects.get(id=course_id)
                student_model.course_id=course
                department=Department.objects.get(id=department_id)
                student_model.department_id=department
                student_model.save()
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect("/edit_student/"+students_id)
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect("/edit_student/"+students_id)
        else:
            form=EditStudentForm(request.POST)
            student=Student.objects.get(admin=students_id)
            return render(request,"admin_template/edit_student_template.html",{"form":form,"id":students_id,"username":student.admin.username})

def manage_session(request):
    return render(request,"admin_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))


def delete_notice(request, id):
    notice = Notice.objects.get(id=id)
    notice.delete()
    return HttpResponseRedirect("/manage_notice")

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_template/admin_profile.html", {"user":user})

def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))



def update_attendance(request):
    subject=Subject.objects.all()
    session_year_id=SessionYearModel.object.all()
    return render(request,"admin_template/update_attendance.html",{"subject":subject,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subject.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,sessionyear_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.date),"session_year_id":attendance_single.sessionyear_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceSave.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.students_id.admin.id,"name":student.students_id.admin.first_name+" "+student.students_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Student.objects.get(admin=stud['id'])
             attendance_report=AttendanceSave.objects.get(students_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"admin_template/leave_view.html",{"leaves":leaves})
def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))
