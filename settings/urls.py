from django.urls import path, re_path
from .views import SettingView, ClosingTimeView

app_name = 'settings'

urlpatterns = [
    path('', SettingView.as_view(), name='index'),
    path('closing-time', ClosingTimeView.as_view(), name='closing_time'),
]