from django.urls import path
from .views import BookingCreateView, BookingDashboardView, BookingStatusUpdateView, ReviewCreateView

app_name = 'bookings'

urlpatterns = [
    path('dashboard/', BookingDashboardView.as_view(), name='dashboard'),
    path('request/<int:worker_id>/', BookingCreateView.as_view(), name='request'),
    path('<int:pk>/status/<str:action>/', BookingStatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='leave_review'),
]
