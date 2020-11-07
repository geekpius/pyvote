from django.urls import path, re_path
from .views import *

app_name = 'voters'

urlpatterns = [
    path('', CreateVoterView.as_view(), name='index'),
    path('view', VoterView.as_view(), name='view'),
    path('verified', VerifiedVoterView.as_view(), name='verified'),
    path('not-verified', NotVerifiedVoterView.as_view(), name='not_verified'),
    path('voted', VotedVoterView.as_view(), name='voted'),
    path('not-voted', NotVotedVoterView.as_view(), name='not_voted'),
    path('table', VoterAjaxTableView.as_view(), name='table'),
    path('<int:id>/update_delete', VoterUpdateDelete.as_view(), name='update_delete'),

    # VERIFICATION
    path('verifications', VerificationView.as_view(), name='verification'),
    path('verifications/verify', VerifyVoterView.as_view(), name='verify'),
    path('verifications/mass-verify', MassVerificationVoterView.as_view(), name='mass_verify'),

]