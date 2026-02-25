from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('worker', 'Worker'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, label="I want to register as a")
    phone = forms.CharField(max_length=15, label="Phone Number", required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), label="Address", required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.user_type = self.cleaned_data['user_type']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.save()
        return user

from django.contrib.auth import get_user_model
User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }
