from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Booking, Review
from .forms import BookingRequestForm, ReviewForm
from apps.workers.models import WorkerProfile

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingRequestForm
    template_name = 'bookings/request.html'
    success_url = reverse_lazy('bookings:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the worker we are booking
        context['worker'] = get_object_or_404(WorkerProfile, id=self.kwargs['worker_id'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['worker'] = get_object_or_404(WorkerProfile, id=self.kwargs['worker_id'])
        return kwargs

    def form_valid(self, form):
        form.instance.customer = self.request.user
        worker_profile = get_object_or_404(WorkerProfile, id=self.kwargs['worker_id'])
        form.instance.worker = worker_profile
        messages.success(self.request, f"Booking request sent to {worker_profile.user.first_name}!")
        return super().form_valid(form)

class BookingDashboardView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/dashboard.html'
    context_object_name = 'bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Split bookings into two context variables
        context['my_bookings'] = Booking.objects.filter(customer=user).order_by('-booking_date')
        
        if hasattr(user, 'worker_profile') and user.worker_profile.skills:
            context['has_profile'] = True
            context['service_requests'] = Booking.objects.filter(worker=user.worker_profile).order_by('-booking_date')
        else:
            context['has_profile'] = False
            context['service_requests'] = Booking.objects.none()
            
        return context

    def get_queryset(self):
        # The main QuerySet is not used heavily anymore since we explicitly
        # provide my_bookings and service_requests in context data.
        return Booking.objects.none()

from django.views.generic import View
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class BookingStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, action):
        booking = get_object_or_404(Booking, pk=pk)
        user = request.user

        # Permission check
        is_customer = booking.customer == user
        is_worker = hasattr(user, 'worker_profile') and booking.worker == user.worker_profile

        if not (is_customer or is_worker):
            messages.error(request, "You do not have permission to modify this booking.")
            return redirect('bookings:dashboard')

        if action == 'cancel' and (is_customer or is_worker) and booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            messages.success(request, "Booking cancelled.")
        elif action == 'confirm' and is_worker and booking.status == 'pending':
            booking.status = 'confirmed'
            messages.success(request, "Booking confirmed.")
        elif action == 'complete' and is_worker and booking.status == 'confirmed':
            booking.status = 'completed'
            messages.success(request, "Booking marked as completed.")
        else:
            messages.error(request, "Invalid action.")

        booking.save()
        
        if is_worker:
            return redirect('/dashboard/?tab=requests')
        return redirect('bookings:dashboard')

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'bookings/review_form.html'
    success_url = reverse_lazy('bookings:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = get_object_or_404(Booking, id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        booking = get_object_or_404(Booking, id=self.kwargs['pk'])
        
        # Verify permissions: only the customer of a completed booking can review
        if booking.customer != self.request.user:
            messages.error(self.request, "You can only review your own bookings.")
            return redirect('bookings:dashboard')
            
        if booking.status != 'completed':
            messages.error(self.request, "You can only review completed jobs.")
            return redirect('bookings:dashboard')
            
        if hasattr(booking, 'review'):
            messages.error(self.request, "You have already reviewed this job.")
            return redirect('bookings:dashboard')

        # Link up relations
        form.instance.booking = booking
        form.instance.reviewer = self.request.user
        form.instance.reviewee = booking.worker
        
        messages.success(self.request, f"Thank you for reviewing {booking.worker.user.first_name}!")
        return super().form_valid(form)
