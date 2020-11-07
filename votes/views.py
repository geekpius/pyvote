from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.template import loader

from django.contrib import messages

from .mixins import VerifiedRequiredMixin

from candidates.models import Position, Candidate
from voters.models import Voter
from .models import Vote, VoteCart
from settings.models import Setting
from .forms import VoteCartForm, VoteForm
import datetime


class VoterLoginView(View):
    template_name = "voters/login.html"

    def get(self, request, *args, **kwargs):
        setting = Setting.objects.filter().first()
        closing_time = datetime.datetime.strptime(setting.closing_time, "%Y-%m-%d %H:%M")
        context = {
            "closing_time": closing_time
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        access_number = request.POST['access_number']
        try:
            voter = Voter.objects.get(access_number=access_number)
            if not voter.is_verified:
                messages.error(request, 'Access number is not verified. Contact verification point.')
            elif voter.is_voted:
                messages.error(request, 'Access number is already voted.')
            else:
                request.session['name'] = voter.name
                request.session['access_number'] = voter.access_number
                request.session['voter'] = voter.id
                request.session['department'] = voter.department
                return redirect('votes:ballot_sheet')
        except Voter.DoesNotExist:
            messages.error(request, 'Access number does not exist.')
            
        setting = Setting.objects.filter().first()
        closing_time = datetime.datetime.strptime(setting.closing_time, "%Y-%m-%d %H:%M")
        context = {
            "closing_time": closing_time
        }
        return render(request, self.template_name, context)


class LogOutView(View):

    def get(self, request, *args, **kwargs):
        del request.session['access_number'] 
        del request.session['name'] 
        del request.session['voter']
        del request.session['department']
        return redirect('votes:index')


class BallotSheetView(VerifiedRequiredMixin, View):
    template_name = "voters/ballot_sheet.html"
    form_class = VoteCartForm

    def get(self, request, *args, **kwargs):
        positions  = Position.objects.all()
        context = {
            'position_list': positions,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            positions = Position.objects.all()
            voter = form.cleaned_data['voter']
            for post in positions:
                if post.name_underscore in request.POST:
                    candidate = request.POST.get(post.name_underscore, False)
                    if VoteCart.objects.filter(voter=voter, position=post.name).count() > 0:
                        voter_cart = VoteCart.objects.get(voter=voter, position=post.name)
                        voter_cart.candidate = candidate
                        voter_cart.save()
                    else:
                        VoteCart.objects.create(voter=voter, candidate=candidate, position=post.name)

        return redirect('votes:preview')


class PreviewView(VerifiedRequiredMixin, View):
    template_name = "voters/preview.html"
    form_class = VoteForm

    def get(self, request, *args, **kwargs):
        voter = request.session['voter']
        carts  = VoteCart.objects.filter(voter=voter)
        context = {
            'cart_list': carts,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            voter = form.cleaned_data['voter']
            candidates = request.POST.getlist("candidates[]")
            if Vote.objects.filter(voter=voter).count() < 1:
                for candidate in candidates:
                    if candidate != "Skipped" and candidate != "No":
                        can = Candidate.objects.get(name=candidate)
                        can.vote = can.vote+1
                        can.save()

                    Vote.objects.create(voter=voter, candidate=candidate)

                current_voter = Voter.objects.get(id=voter.id)
                current_voter.is_voted = True
                current_voter.save()
        return redirect('votes:notification')


class ChangeCandidateView(VerifiedRequiredMixin, View):
    template_name = "voters/change.html"

    def get(self, request, post, *args, **kwargs):
        position_name = post.title().replace('-',' ')
        position = get_object_or_404(Position, name=position_name)
        context = {
            'position': position,
        }
        return render(request, self.template_name, context)


class NotificationView(VerifiedRequiredMixin, View):
    template_name = "voters/notification.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

