from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from .forms import SigninForm, AccountCreateForm
from candidates.models import Position, Candidate
from voters.models import Voter
from votes.models import Vote
from .models import User


class SignInView(View):
    """ authenticate user on siging in """
    form_class = SigninForm
    template_name = "admins/auth/login.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_active:
            return redirect("accounts:dashboard")
        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user.is_active:
                if user.is_staff or user.is_superuser:
                    messages.error(request, 'You are not authourized.')
                else:
                    login(request, user)
                    redirect_url = self.request.GET.get('redirect_to', 'accounts:dashboard')
                    return redirect(redirect_url)
            else:
                messages.error(request, 'Your account is not activated.')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """ log user out of the system """
    def get(self, request):
        logout(request)
        return redirect('accounts:sign_in')


class DashboardView(LoginRequiredMixin, View):
    """
        This class makes get request to the dashboard
        It gets data base on your role
    """
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = 'admins/dashboard/index.html'

    def get(self, request, *args, **kwargs):
        count_positions = Position.objects.count()
        count_candidates = Candidate.objects.count()
        count_voters = Voter.objects.count()
        count_votes = Vote.objects.count()
        
        context = {
            'count_positions': count_positions,
            'count_candidates': count_candidates,
            'count_voters': count_voters,
            'count_votes': count_votes
        }

        return render(request, self.template_name, context)


class UserAjaxTableView(LoginRequiredMixin, View):
    """ get user data on ajax request """

    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        template = loader.get_template("admins/accounts/account_table.html")
        users = User.objects.filter(is_superuser=False, is_staff=False)
        context = {
            "user_list": users,
        }
        return HttpResponse(template.render(context, self.request))


class UserView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"
    template_name = 'admins/accounts/index.html'
    form_class = AccountCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                
                password = user.set_password(password)
                user.save()
                role = request.POST['role']
                u = User.objects.get(id=user.id)
                if role == 'admin':
                    u.is_admin = True
                    u.is_ec = True
                    u.is_verifier = True
                elif role == 'ec':
                    u.is_ec = True
                    u.is_verifier = True
                else:
                    u.is_verifier = True
                
                u.save()
                return JsonResponse({'message': 'success'})

            return JsonResponse({'message': 'Username already exist'})


class UserUpdateDeleteView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            User.objects.get(id=id).delete()
            return JsonResponse({'message': 'success'})
    
    def post(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            user = User.objects.get(id=id)
            role = request.POST['role']
            if role == 'admin':
                user.is_admin = True
                user.is_ec = True
                user.is_verifier = True
            elif role == 'ec':
                user.is_admin = False
                user.is_ec = True
                user.is_verifier = True
            else:
                user.is_admin = False
                user.is_ec = False
                user.is_verifier = True
            
            user.save()
            return JsonResponse({'message': 'success'})


class UserToggleBlockView(LoginRequiredMixin, View):
    login_url = "accounts:sign_in"
    redirect_field_name = "redirect_to"

    def get(self, request, id, *args, **kwargs):
        if self.request.is_ajax():
            user = User.objects.get(id=id)
            if user.is_active:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()

            return JsonResponse({'message': 'success'})