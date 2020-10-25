from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.template import loader
from .forms import DepartmentForm
from .models import Department


class DepartmentAjaxTableView(LoginRequiredMixin, View):
    """ get department data on ajax request """

    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        template = loader.get_template("admins/departments/department_table.html")
        departments = Department.objects.all()
        context = {
            "department_list": departments,
        }
        return HttpResponse(template.render(context, self.request))


class DepartmentView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/departments/department.html"
    form_class = DepartmentForm

    def get(self, request, *args, **kwargs):
        if not request.user.get_setting.is_department:
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                department = form.save(commit=False)
                name = form.cleaned_data['name']

                department.save()
                return JsonResponse({'message': 'success'})

            return JsonResponse({'message': 'Wrong input field'})


class DepartmentUpdateDelete(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    form_class = DepartmentForm

    def get(self, request, id, *args, **kwargs):
        Department.objects.get(id=id).delete()
        return JsonResponse({'message': 'success'})

    def post(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            department = Department.objects.get(id=id)
            data = { "name": department.name }
            form = self.form_class(request.POST, initial=data)
            if form.is_valid():
                name = form.cleaned_data['name']

                if form.has_changed():
                    department.name = name
                    department.save()
                    return JsonResponse({'message': 'success'})
                
                return JsonResponse({'message': 'No input changed'})

            return JsonResponse({'message': 'Wrong input field'})
            

