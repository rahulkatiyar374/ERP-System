from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from erp.models import CustomUser, Faculty, Student, Subject, Notes


class UserModel(UserAdmin):
    pass

class AdminFaculty(admin.ModelAdmin):
    pass

class AdminStudent(admin.ModelAdmin):
    pass
class AdminSubject(admin.ModelAdmin):
    pass
class AdminNotes(admin.ModelAdmin):
    pass
admin.site.register(CustomUser,UserModel)
admin.site.register(Faculty, AdminFaculty)
admin.site.register(Student, AdminStudent)
admin.site.register(Subject, AdminSubject)
admin.site.register(Notes, AdminNotes)
#admin.site.register(Subject, AdminSubject)