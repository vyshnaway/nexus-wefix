from django.urls import path
from .views import WorkerListView, WorkerProfileUpdateView

app_name = 'workers'

urlpatterns = [
    path('', WorkerListView.as_view(), name='worker_list'),
    path('profile/', WorkerProfileUpdateView.as_view(), name='profile_update'),
]
