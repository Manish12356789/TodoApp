from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from django import forms
from .models import Item, UserProfile


class TODOform(forms.ModelForm):
    # user = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False))
    field = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'id': 'todo-list-item', 'placeholder': 'Enter your todo...'}))


    class Meta:
        model = Item
        fields = ['field']


class UserForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'input--style-3', 'placeholder': 'Enter Your Username...'}))

    email = forms.EmailField(label='', error_messages={'required': 'Enter the valid email address.'},
                             widget=forms.TextInput(
                                 attrs={'class': 'input--style-3', 'placeholder': 'Enter Your Email...'}))
    password1 = forms.CharField(label='', error_messages={'required': 'Enter the strong password.'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input--style-3', 'placeholder': 'Enter Your Password...'}))
    password2 = forms.CharField(label='', error_messages={'required': 'Password not matched.'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input--style-3', 'placeholder': 'Confirm Your Password...'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='User Name',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(label='Profile Picture')

    class Meta:
        model = UserProfile
        fields = ('profile_pic',)


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='',
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'input--style-3', 'placeholder': 'Your Old Password ...'}))
    new_password1 = forms.CharField(label='',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'input--style-3', 'placeholder': 'Your New Password...'}))
    new_password2 = forms.CharField(label='',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'input--style-3',
                                               'placeholder': 'Confirm Your New Password...'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
