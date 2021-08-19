from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from erp.forms import EditMarkForm
from erp.models import Student, Subject, Mark


class EditResultViewClass(View):
    def get(self,request,*args,**kwargs):
        staff_id=request.user.id
        edit_result_form=EditMarkForm(faculty_id=staff_id)
        return render(request,"faculty_template/edit_mark.html",{"form":edit_result_form})

    def post(self,request,*args,**kwargs):
        form=EditMarkForm(faculty_id=request.user.id,data=request.POST)
        if form.is_valid():
            student_admin_id = form.cleaned_data['student_ids']
            sessional_1 = form.cleaned_data['sessional_marks']
            sessional_2 = form.cleaned_data['sessionaltwo_marks']
            ta = form.cleaned_data['ta_marks']
            mock = form.cleaned_data['mock_marks']
            subject_id = form.cleaned_data['subject_id']

            student_obj = Student.objects.get(admin=student_admin_id)
            subject_obj = Subject.objects.get(id=subject_id)
            result=Mark.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.sessional_1=sessional_1
            result.sessional_2=sessional_2
            result.ta = ta
            result.mock = mock
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("edit_mark"))
        else:
            messages.error(request, "Failed to Update Result")
            form=EditMarkForm(request.POST,faculty_id=request.user.id)
            return render(request,"faculty_template/edit_mark.html",{"form":form})


