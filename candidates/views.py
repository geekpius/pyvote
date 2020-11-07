from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.template import loader
from .forms import (PositionForm, CandidateForm, CandidateUpdateForm, CandidateImageUpdateForm)
from .models import Position, Candidate
from departments.models import Department
from votes.models import Vote
from voters.models import Voter
from settings.models import Setting
import os

from django.db.models import Sum, Q



class CandidateAjaxTableView(LoginRequiredMixin, View):
    """ get candidate data on ajax request """

    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        template = loader.get_template("admins/candidates/candidate_table.html")
        candidates = Candidate.objects.all()
        context = {
            "candidate_list": candidates,
        }
        return HttpResponse(template.render(context, self.request))


class CandidateView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/candidates/candidate.html"
    form_class = CandidateForm

    def get(self, request, *args, **kwargs):
        if request.user.get_setting.is_department:
            department = Department.objects.filter().values('name')
        else:
            department = None

        position = Position.objects.filter().values('id','name')
        context = {
            "position_list": position,
            "department_list": department
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                candidate = form.save(commit=False)
                position = form.cleaned_data['position']
                count_can = Candidate.objects.filter(position=position).count()
                if position.max_con == count_can:
                    return JsonResponse({'message': f"{position} position has reached it's maximum"})
                else:
                    candidate.save()
                    return JsonResponse({'message': 'success'})

            return JsonResponse({'message': 'Wrong input field'})


class CandidateUpdateDelete(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    form_class = CandidateUpdateForm

    def get(self, request, id, *args, **kwargs):
        candidate = Candidate.objects.get(id=id)
        # check if image field path exist in directory
        if candidate.image and os.path.exists(candidate.image.path):
            # remove from path
            os.remove(candidate.image.path)
        candidate.delete()
        return JsonResponse({'message': 'success'})

    def post(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            candidate = Candidate.objects.get(id=id)
            data = { "name": candidate.name, "gender":candidate.gender, "position":candidate.position, "department":candidate.department }
            form = self.form_class(request.POST, initial=data)
            if form.is_valid():
                name = form.cleaned_data['name']
                gender = form.cleaned_data['gender']
                position = form.cleaned_data['position']
                department = form.cleaned_data['department']

                if form.has_changed():
                    candidate.name = name
                    candidate.gender = gender
                    candidate.position = position
                    candidate.department = department
                    candidate.save()
                    return JsonResponse({'message': 'success'})
                
                return JsonResponse({'message': 'No input changed'})

            return JsonResponse({'message': 'Wrong input field'})


class CandidateImageUpdate(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    form_class = CandidateImageUpdateForm

    def post(self, request, id, *args, **kwargs):
        if request.is_ajax():
            candidate = Candidate.objects.get(id=id)
            data = {"image": candidate.image}
            form = self.form_class(request.POST, request.FILES, initial=data)
            if form.is_valid():
                image = form.cleaned_data['image']
                # check if image field is not empty
                if candidate.image:
                    # check if image field path exist in directory
                    if os.path.exists(candidate.image.path):
                        # remove from path and reupdate with the new one
                        os.remove(candidate.image.path)
                        candidate.image = image
                        candidate.save()
                        return JsonResponse({"message":"success"})
                    else:
                        # update new image if theres no image in directory
                        candidate.image = image
                        candidate.save()
                        return JsonResponse({"message":"success"})
                else:
                    # update new image if there no image in the image field
                    candidate.image = image
                    candidate.save()
                    return JsonResponse({"message":"success"})

            return JsonResponse({"message":"Validating image failed"})


class CandidateAjaxVotersView(LoginRequiredMixin, View):
    """ get candidate data on ajax request """

    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, id, *args, **kwargs):
        template = loader.get_template("admins/candidates/candidate_voters.html")
        candidate = Candidate.objects.get(id=id)
        voters = Vote.objects.filter(candidate=candidate.name)
        context = {
            "voter_list": voters,
            "candidate": candidate.name.title(),
        }
        return HttpResponse(template.render(context, self.request))


            
##### POSITIONS #####
class PositionAjaxTableView(LoginRequiredMixin, View):
    """ get postion data on ajax request """

    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        template = loader.get_template("admins/positions/position_table.html")
        positions = Position.objects.all()
        context = {
            "position_list": positions,
        }
        return HttpResponse(template.render(context, self.request))


class PositionView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/positions/position.html"
    form_class = PositionForm

    def get(self, request, *args, **kwargs):
        if request.user.get_setting.is_department:
            departments = Department.objects.filter().values('name')
        else:
            department = None
        context = {
            "department_list": departments
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'success'})

            return JsonResponse({'message': 'Wrong input field'})


class PositionUpdateDelete(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    form_class = PositionForm

    def get(self, request, id, *args, **kwargs):
        Position.objects.get(id=id).delete()
        return JsonResponse({'message': 'success'})

    def post(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            position = Position.objects.get(id=id)
            data = { "name": position.name, "position_type":position.position_type, "max_con":position.max_con, "winning_format":position.winning_format }
            form = self.form_class(request.POST, initial=data)
            if form.is_valid():
                name = form.cleaned_data['name']
                position_type = form.cleaned_data['position_type']
                max_con = form.cleaned_data['max_con']
                winning_format = form.cleaned_data['winning_format']

                if form.has_changed():
                    position.name = name
                    position.position_type = position_type
                    position.max_con = max_con
                    position.winning_format = winning_format
                    position.save()
                    return JsonResponse({'message': 'success'})
                
                return JsonResponse({'message': 'No input changed'})

            return JsonResponse({'message': 'Wrong input field'})



##### RESULTS #####
class SingleResultView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/results/single.html"

    def get(self, request, *args, **kwargs):
        positions = Position.objects.all().values("id", "name")
        context = {
            "position_list": positions
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            template = loader.get_template("admins/results/single_results.html")
            post_id = request.POST['position']
            position = Position.objects.get(id=post_id)
            setting = Setting.objects.filter().values("title", "year").first()

            if position.position_type == 'general':
                total_voters = Voter.objects.count()
                total_voted = Voter.objects.filter(is_voted=True).count()
                total_not_voted = Voter.objects.filter(is_voted=False).count()
                sum_votes = Candidate.objects.filter(position=position).aggregate(votes=Sum("vote"))
                candidates = Candidate.objects.filter(position=position)
            else:
                total_voters = Voter.objects.filter(department=position.position_type.lower()).count()
                total_voted = Voter.objects.filter(is_voted=True, department=position.position_type.lower()).count()
                total_not_voted = Voter.objects.filter(is_voted=False, department=position.position_type.lower()).count()
                sum_votes = Candidate.objects.filter(position=position, department=position.position_type.lower()).aggregate(votes=Sum("vote"))
                candidates = Candidate.objects.filter(position=position, department=position.position_type.lower())

            context = {
                "position": position,
                "setting": setting,
                "total_voters": total_voters,
                "total_voted": total_voted,
                "total_not_voted": total_not_voted,
                "sum_votes": sum_votes,
                "candidate_list": candidates,
            }
            return HttpResponse(template.render(context, self.request))


class AllResultView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = "admins/results/all.html"

    def get(self, request, *args, **kwargs):
        postions = Position.objects.all()
        setting = Setting.objects.filter().values("title", "year").first()

        total_voters = Voter.objects.count()
        total_voted = Voter.objects.filter(is_voted=True).count()
        total_not_voted = Voter.objects.filter(is_voted=False).count()
        total_vote_casted = Vote.objects.count()
        total_skip_votes = Vote.objects.filter(candidate="Skipped").count()
        total_valid_votes = Vote.objects.filter(~Q(candidate="Skipped")).count()
        context = {
            "position_list": postions,
            "setting": setting,
            "total_voters": total_voters,
            "total_voted": total_voted,
            "total_not_voted": total_not_voted,
            "total_vote_casted": total_vote_casted,
            "total_skip_votes": total_skip_votes,
            "total_valid_votes": total_valid_votes,
        }
        return render(request, self.template_name, context)

