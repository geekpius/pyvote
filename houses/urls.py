from django.urls import path, re_path
from .views import *

app_name = 'houses'

urlpatterns = [
    path('', HouseView.as_view(), name='index'),
    path('table', HouseAjaxTableView.as_view(), name='table'),
    path('<int:id>/update-delete', HouseUpdateDelete.as_view(), name='update_delete'),
]