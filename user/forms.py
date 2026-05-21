from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)

from .models import CustomUser,UserProfile

class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'picture',
            'password1',
            'password2'
        ]


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email'
            }
        )
    )


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'picture',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ism'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiya'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Telefon raqam'}),
        }

class UserProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': "O'zingiz haqingizda yozing...",
            'rows': 4
        })
    )

    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-input',
            'placeholder': 'https://example.com'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'website']