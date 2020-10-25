from django.urls import path, re_path
from .views import *

app_name = 'departments'

urlpatterns = [
    path('', DepartmentView.as_view(), name='index'),
    path('table', DepartmentAjaxTableView.as_view(), name='table'),
    path('<int:id>/update-delete', DepartmentUpdateDelete.as_view(), name='update_delete'),
]