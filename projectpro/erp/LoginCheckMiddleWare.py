from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "erp.admin_views":
                    pass
                elif modulename == "erp.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "erp.faculty_views" or modulename == "erp.EditMarkViewClass":
                    pass
                elif modulename == "erp.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("faculty_home"))
            elif user.user_type == "3":
                if modulename == "erp.student_views":
                    pass
                elif modulename == "erp.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))