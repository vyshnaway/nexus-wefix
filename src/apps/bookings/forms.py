from django import forms
from .models import Booking, Review

class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'booking_date', 'location']
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full service address'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        worker = kwargs.pop('worker', None)
        super().__init__(*args, **kwargs)
        if worker and worker.skills:
            from apps.workers.models import Service
            self.fields['service'].queryset = Service.objects.filter(category__in=worker.skills)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}),
        }
