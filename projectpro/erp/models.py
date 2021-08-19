from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Faculty"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()

class Course(models.Model):
    id=models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=50)
    c_duration = models.IntegerField()
    objects = models.Manager()


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    sub_code = models.CharField(max_length=10)
    sub_name = models.CharField(max_length=50)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    faculty_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()


class Department(models.Model):
    id=models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    d_name = models.CharField(max_length=50)
    objects = models.Manager()

class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mob_no = models.IntegerField()
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    objects = models.Manager()

class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.IntegerField(default=2020)
    session_end_year=models.IntegerField(default=2024)
    object=models.Manager()

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_no = models.IntegerField()
    mob_no = models.IntegerField()
    pmob_no = models.IntegerField()
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    gender = models.CharField(max_length=255)

    address = models.TextField()
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    sessionyear_id = models.ForeignKey(SessionYearModel, on_delete=models.DO_NOTHING)
    objects = models.Manager()

class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    detail = models.TextField()
    notes = models.FileField()
    objects = models.Manager()

class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    detail = models.TextField()
    file = models.FileField()
    objects = models.Manager()

class Mark(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    sessional_1 = models.IntegerField(default=00)
    sessional_2 = models.IntegerField(default=00)
    ta = models.IntegerField(default=00)
    mock = models.IntegerField(default=00)
    objects = models.Manager()

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    sessionyear_id = models.ForeignKey(SessionYearModel, on_delete=models.DO_NOTHING)
    date = models.DateField(default=1)
    objects = models.Manager()

class AttendanceSave(models.Model):
    id = models.AutoField(primary_key=True)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    students_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    objects = models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Faculty.objects.create(admin=instance, department_id=Department.objects.get(id=1), mob_no="100")
        if instance.user_type==3:
            Student.objects.create(admin=instance,course_id=Course.objects.get(id=1),department_id=Department.objects.get(id=1),sessionyear_id=SessionYearModel.object.get(id=1),address="",gender="",mob_no="100",pmob_no="100",roll_no="11",fname="",mname="")
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.faculty.save()
    if instance.user_type==3:
        instance.student.save()

