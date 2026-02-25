from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm
from apps.workers.models import WorkerProfile
from apps.workers.forms import WorkerProfileForm

@login_required
def profile_view(request):
    user = request.user
    
    # Get or initialize the worker profile
    try:
        worker_profile = user.worker_profile
    except WorkerProfile.DoesNotExist:
        worker_profile = WorkerProfile(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        worker_form = WorkerProfileForm(request.POST, instance=worker_profile)
        
        # Check which form was submitted based on a hidden input or just process both
        if 'update_user' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your personal information has been updated.')
                return redirect('accounts:profile')
        
        elif 'update_worker' in request.POST:
            if worker_form.is_valid():
                worker_instance = worker_form.save(commit=False)
                worker_instance.user = user
                worker_instance.save()
                
                # Upgrade user to worker if they aren't already
                if user.user_type != 'worker':
                    user.user_type = 'worker'
                    user.save()
                    messages.success(request, 'You are now registered as a Professional! Your profile will be reviewed.')
                else:
                    messages.success(request, 'Your professional profile has been updated.')
                
                return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        worker_form = WorkerProfileForm(instance=worker_profile)

    context = {
        'user_form': user_form,
        'worker_form': worker_form,
        'has_skills': bool(worker_profile.skills),
    }
    return render(request, 'accounts/profile.html', context)
