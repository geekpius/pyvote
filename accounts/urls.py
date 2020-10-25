from django.urls import path, re_path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign_in'),
    path('sign-out', LogoutView.as_view(), name='sign_out'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),

    # USERS
    path('accounts', UserView.as_view(), name='user'),
    path('table', UserAjaxTableView.as_view(), name='table'),
    path('accounts/<int:id>/update-delete', UserUpdateDeleteView.as_view(), name='update_delete'),
    path('accounts/<int:id>/toggle-block', UserToggleBlockView.as_view(), name='toggle_block'),
]