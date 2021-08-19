"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import path
from erp.EditMarkViewClass import EditResultViewClass
from erp import views, admin_views, faculty_views, student_views
from projectpro import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo', views.showDemoPage),
    path('', views.ShowLoginPage, name="show_login"),
    path('get_user_detail', views.GetUserDetails),
    path('logout_user', views.logout_user),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin_home', admin_views.admin_home, name="admin_home"),
    path('add_faculty', admin_views.add_faculty,name="add_faculty"),
    path('add_faculty_save', admin_views.add_faculty_save,name="add_faculty_save"),
    path('add_course', admin_views.add_course,name="add_course"),
    path('add_course_save', admin_views.add_course_save,name="add_course_save"),
    path('add_department', admin_views.add_department,name="add_department"),
    path('add_department_save', admin_views.add_department_save,name="add_department_save"),
    path('add_subject', admin_views.add_subject,name="add_subject"),
    path('add_subject_save', admin_views.add_subject_save,name="add_subject_save"),
    path('add_notice', admin_views.add_notice,name="add_notice"),
    path('add_notice_save', admin_views.add_notice_save,name="add_notice_save"),
    path('add_student', admin_views.add_student, name="add_student"),
    path('add_student_save', admin_views.add_student_save, name="add_student_save"),
    path('manage_faculty', admin_views.manage_faculty,name="manage_faculty"),
    path('manage_student', admin_views.manage_student,name="manage_student"),
    path('manage_notice', admin_views.manage_notice,name="manage_notice"),
    path('manage_course', admin_views.manage_course,name="manage_course"),
    path('manage_department', admin_views.manage_department,name="manage_department"),
    path('manage_subject', admin_views.manage_subject,name="manage_subject"),
    path('edit_faculty/<str:facultys_id>', admin_views.edit_faculty),
    path('edit_faculty_save', admin_views.edit_faculty_save,name="edit_faculty_save"),
    path('edit_course/<str:courses_id>', admin_views.edit_course),
    path('edit_course_save', admin_views.edit_course_save,name="edit_course_save"),
    path('edit_department/<str:departments_id>', admin_views.edit_department),
    path('edit_department_save', admin_views.edit_department_save,name="edit_department_save"),
    path('edit_subject/<str:subjects_id>', admin_views.edit_subject),
    path('edit_subject_save', admin_views.edit_subject_save,name="edit_subject_save"),
    path('delete_notice/<int:id>', admin_views.delete_notice),
    path('edit_student/<str:students_id>', admin_views.edit_student,name="edit_student"),
    path('edit_student_save', admin_views.edit_student_save, name="edit_student_save"),
    path('manage_session', admin_views.manage_session,name="manage_session"),
    path('add_session_save', admin_views.add_session_save,name="add_session_save"),
    path('admin_profile', admin_views.admin_profile, name="admin_profile"),
    path('admin_profile_save', admin_views.admin_profile_save, name="admin_profile_save"),
    path('update_attendance', admin_views.update_attendance, name="update_attendance"),
    path('get_attendance_dates', admin_views.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', admin_views.get_attendance_student, name="get_attendance_student"),
    path('save_updateattendance_data', admin_views.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_leave_view', admin_views.staff_leave_view,name="staff_leave_view"),
    path('staff_disapprove_leave/<str:leave_id>', admin_views.staff_disapprove_leave,name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', admin_views.staff_approve_leave,name="staff_approve_leave"),




    path('faculty_home', faculty_views.faculty_home, name="faculty_home"),
    path('add_staff_notice', faculty_views.add_staff_notice),
    path('add_staff_notice_save', faculty_views.add_staff_notice_save),
    path('add_notes', faculty_views.add_notes),
    path('add_notes_save', faculty_views.add_notes_save),
    path('manage_notes', faculty_views.manage_notes),
    path('delete_notes/<int:id>',faculty_views.delete_notes),
    path('show_subject', faculty_views.show_subject,name="show_subject"),
    path('staff_apply_leave', faculty_views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', faculty_views.staff_apply_leave_save, name="staff_apply_leave_save"),
    #path('take_attendance', faculty_views.take_attendance),
    #path('get_student/<int:id>', faculty_views.get_student, name="get_student"),
    path('get_students', faculty_views.get_students, name="get_students"),
    path('save_attendance_data', faculty_views.save_attendance_data, name="save_attendance_data"),
    path('staff_fcmtoken_save', faculty_views.staff_fcmtoken_save, name="staff_fcmtoken_save"),
    path('faculty_profile', faculty_views.faculty_profile, name="faculty_profile"),
    path('faculty_profile_save', faculty_views.faculty_profile_save, name="faculty_profile_save"),
    path('faculty_add_mark', faculty_views.faculty_add_mark, name="faculty_add_mark"),
    path('save_student_mark', faculty_views.save_student_mark, name="save_student_mark"),
    path('edit_mark', EditResultViewClass.as_view(), name="edit_mark"),
    path('fetch_result_student', faculty_views.fetch_result_student, name="fetch_result_student"),
    path('show', faculty_views.show,name="show"),
    path('student/<int:id>',faculty_views.student, name="student"),


   #student url

    path('student_home', student_views.student_home, name="student_home"),
    path('student_fcmtoken_save', student_views.student_fcmtoken_save, name="student_fcmtoken_save"),
    path('show_notes', student_views.show_notes),
    path('show_notice', student_views.show_notice),
    url(r'^download/(?P<path>.*)$', serve, {'document root': settings.MEDIA_ROOT}),
    path('student_profile', student_views.student_profile,name="student_profile"),
    path('student_profile_save', student_views.student_profile_save,name="student_profile_save"),
    path('student_view_result',student_views.student_view_result,name="student_view_result"),
    path('student_view_attendance', student_views.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', student_views.student_view_attendance_post, name="student_view_attendance_post"),


]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
