from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.template import loader

from .forms import SettingForm
from .models import Setting



class SettingView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/settings/index.html"
    form_class = SettingForm

    def get(self, request, *args, **kwargs):
        setting = Setting.objects.filter().first()
        context ={
            'setting': setting
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                year = form.cleaned_data['year']
                is_department = form.cleaned_data['is_department']
                obj, created = Setting.objects.update_or_create(defaults={'title':title, 'year':year, 'is_department': is_department})
                if created:
                    return JsonResponse({'message': 'success'})
                else:
                    return JsonResponse({'message': 'update'})

            return JsonResponse({'message': 'Some input fields are required'})


class ClosingTimeView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/settings/index.html"
    
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            closing_date = request.POST['closing_date']
            closing_time = request.POST['closing_time']
            end_date = f"{closing_date} {closing_time}"

            setting = Setting.objects.filter().first()
            setting.closing_time = end_date
            setting.save()
            return JsonResponse({'message': 'success'})


