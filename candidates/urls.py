from django.urls import path, re_path
from .views import *

app_name = 'candidates'

urlpatterns = [
    path('', CandidateView.as_view(), name='index'),
    path('table', CandidateAjaxTableView.as_view(), name='table'),
    path('<int:id>/update-delete', CandidateUpdateDelete.as_view(), name='update_delete'),
    path('<int:id>/upload', CandidateImageUpdate.as_view(), name='upload'),
    path('<int:id>/voters', CandidateAjaxVotersView.as_view(), name='voters'),

    # positions
    path('positions', PositionView.as_view(), name='position'),
    path('positions/table', PositionAjaxTableView.as_view(), name='position_table'),
    path('positions/<int:id>/update-delete', PositionUpdateDelete.as_view(), name='postision_update_delete'),

    # results
    path('results/single', SingleResultView.as_view(), name='single'),
    path('results/all', AllResultView.as_view(), name='all'),
    path('results/winners', WinnerResultView.as_view(), name='winners'),
]