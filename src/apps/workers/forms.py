from django import forms
from .models import WorkerProfile

class WorkerProfileForm(forms.ModelForm):
    # We will use a comma-separated string for simplicity in the UI, then convert to list
    skills_input = forms.CharField(
        label="Skills (comma separated)", 
        help_text="e.g. Plumbing, electrical, carpentry",
        widget=forms.TextInput(attrs={'placeholder': 'Plumbing, Roofing, Painting'})
    )

    class Meta:
        model = WorkerProfile
        fields = ['location', 'hourly_rate']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'City or Region'}),
            'hourly_rate': forms.NumberInput(attrs={'placeholder': '50.00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['skills_input'] = ", ".join(self.instance.skills)

    def save(self, commit=True):
        instance = super().save(commit=False)
        skills_str = self.cleaned_data.get('skills_input', '')
        instance.skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        if commit:
            instance.save()
        return instance
