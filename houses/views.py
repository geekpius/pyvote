from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.template import loader
from .forms import HouseForm
from .models import House


class HouseAjaxTableView(LoginRequiredMixin, View):
    """ get house data on ajax request """

    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        template = loader.get_template("admins/houses/house_table.html")
        houses = House.objects.all()
        context = {
            "house_list": houses,
        }
        return HttpResponse(template.render(context, self.request))


class HouseView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/houses/house.html"
    form_class = HouseForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                house = form.save(commit=False)
                name = form.cleaned_data['name']

                house.save()
                return JsonResponse({'message': 'success'})

            return JsonResponse({'message': 'Wrong input field'})


class HouseUpdateDelete(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    form_class = HouseForm

    def get(self, request, id, *args, **kwargs):
        House.objects.get(id=id).delete()
        return JsonResponse({'message': 'success'})

    def post(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            house = House.objects.get(id=id)
            data = { "name": house.name }
            form = self.form_class(request.POST, initial=data)
            if form.is_valid():
                name = form.cleaned_data['name']

                if form.has_changed():
                    house.name = name
                    house.save()
                    return JsonResponse({'message': 'success'})
                
                return JsonResponse({'message': 'No input changed'})

            return JsonResponse({'message': 'Wrong input field'})
            

