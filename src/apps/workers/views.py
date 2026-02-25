from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import WorkerProfile
from .forms import WorkerProfileForm

class WorkerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkerProfile
    form_class = WorkerProfileForm
    template_name = 'workers/profile_form.html'
    success_url = reverse_lazy('bookings:dashboard')

    def get_object(self, queryset=None):
        try:
            return self.request.user.worker_profile
        except WorkerProfile.DoesNotExist:
            return WorkerProfile(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your professional profile has been updated.")
        return super().form_valid(form)

class WorkerListView(LoginRequiredMixin, ListView):
    model = WorkerProfile
    template_name = 'workers/worker_list.html'
    context_object_name = 'workers'

    def get_queryset(self):
        from django.db.models import Avg
        qs = super().get_queryset().filter(is_verified=True).exclude(user=self.request.user).select_related('user').annotate(
            avg_rating=Avg('reviews__rating')
        )
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(skills__icontains=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.GET.get('category', '')
        
        # Get unique skills across all verified profiles
        profiles = WorkerProfile.objects.filter(is_verified=True).values_list('skills', flat=True)
        all_skills = set()
        for skills_list in profiles:
            if skills_list:
                for skill in skills_list:
                    all_skills.add(skill.strip())
        context['all_skills'] = sorted(list(all_skills))
        
        return context
