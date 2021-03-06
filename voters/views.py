from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.template import loader
from .forms import VoterForm, VoterUpdateForm
from .models import Voter
from departments.models import Department
from settings.models import Setting



class VoterAjaxTableView(LoginRequiredMixin, View):
    """ get voters data on ajax request """

    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        template = loader.get_template("admins/voters/voter_table.html")
        voters = Voter.objects.all()
        context = {
            "voter_list": voters,
        }
        return HttpResponse(template.render(context, self.request))


class CreateVoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/voters/voter.html"
    form_class = VoterForm

    def get(self, request, *args, **kwargs):        
        if request.user.get_setting.is_department:
            department = Department.objects.filter().values('name')
        else:
            department = None

        context = {
            "department_list": department,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'success'})

            return JsonResponse({'message': 'Access number already exist'})


class VoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/voters/view.html"

    def get(self, request, *args, **kwargs):
        department = Department.objects.filter().values('name')
        context = {
            "department_list": department,
        }
        return render(request, self.template_name, context)


class VerifiedVoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/voters/verified.html"

    def get(self, request, *args, **kwargs):
        voters = Voter.objects.filter(is_verified=True)
        context = {
            "voter_list": voters,
        }
        return render(request, self.template_name, context)


class NotVerifiedVoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/voters/not_verified.html"

    def get(self, request, *args, **kwargs):
        voters = Voter.objects.filter(is_verified=False)
        context = {
            "voter_list": voters,
        }
        return render(request, self.template_name, context)


class VotedVoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/voters/voted.html"

    def get(self, request, *args, **kwargs):
        voters = Voter.objects.filter(is_voted=True)
        context = {
            "voter_list": voters,
        }
        return render(request, self.template_name, context)


class NotVotedVoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/voters/not_voted.html"

    def get(self, request, *args, **kwargs):
        voters = Voter.objects.filter(is_voted=False)
        context = {
            "voter_list": voters,
        }
        return render(request, self.template_name, context)


class VoterUpdateDelete(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    form_class = VoterUpdateForm

    def get(self, request, id, *args, **kwargs):
        Voter.objects.get(id=id).delete()
        return JsonResponse({'message': 'success'})

    def post(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            voter = Voter.objects.get(id=id)
            data = { "name": voter.name, "gender":voter.gender, "department":voter.department }
            form = self.form_class(request.POST, initial=data)
            if form.is_valid():
                name = form.cleaned_data['name']
                gender = form.cleaned_data['gender']
                department = form.cleaned_data['department']

                if form.has_changed():
                    voter.name = name
                    voter.gender = gender
                    voter.department = department
                    voter.save()
                    return JsonResponse({'message': 'success'})
                
                return JsonResponse({'message': 'No input changed'})

            return JsonResponse({'message': 'Wrong input field'})


###### VERIFICATION ######
class VerificationView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/voters/verification.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            access_number = request.POST['access_number']
            try:
                voter = Voter.objects.get(access_number=access_number)
            except Voter.DoesNotExist:
                voter = None
                
            if voter:
                if voter.is_verified and not voter.is_voted:
                    return JsonResponse({'message':'verified'})
                elif voter.is_verified and voter.is_voted:
                    return JsonResponse({'message':'voted'})
                else:
                    return JsonResponse({
                        'id': voter.id,
                        'access_number': voter.access_number,
                        'name': voter.name,
                        'gender': voter.get_gender,
                        'department': voter.department,
                        'is_verified': voter.get_verified,
                        'is_voted': voter.get_voted,
                    })
            else:
                return JsonResponse({'message':'empty'})


class VerifyVoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            id = request.POST['id']
            voter = Voter.objects.get(id=id)
            voter.is_verified = True
            voter.save()
            return JsonResponse({'message':'success'})


class MassVerificationVoterView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            count_voter = Voter.objects.filter(is_verified=False).count()
            if count_voter > 0:
                Voter.objects.filter(is_verified=False).update(is_verified=True)
                return JsonResponse({'message':'success', 'count':count_voter})
            else:
                return JsonResponse({'message':'error', 'count':count_voter})
