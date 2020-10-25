from django.urls import path, re_path
from .views import *

app_name = 'votes'

urlpatterns = [
    path('', VoterLoginView.as_view(), name='index'),
    path('ballotsheet', BallotSheetView.as_view(), name='ballot_sheet'),
    path('preview', PreviewView.as_view(), name='preview'),
    path('change/<str:post>', ChangeCandidateView.as_view(), name='change'),
    path('notification', NotificationView.as_view(), name='notification'),
    path('logout', LogOutView.as_view(), name='logout'),

]