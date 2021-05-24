from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from django import forms
from django.forms import TextInput, PasswordInput, Select
from django.forms.forms import Form
from django.forms.models import ModelChoiceField
from .models import Item, UserProfile


class TODOform(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['field']
        labels = { 
            'field': '',
         }
        widgets = {
            'field': TextInput(attrs={'id': 'todo-list-item','type':'text', 'placeholder': 'Enter your todo...'}),
        }

class StatusForm(forms.ModelForm):
    class Meta:
        CHOICES= (
        ('completed', 'Completed'),
        ('in-progress', 'In-Progress'),
        ('remaining', 'Remaining'),
        )

        model = Item
        fields = ['status']
        widgets = {
            'status': Select(attrs={'class':'user-select btn-block'}, choices=CHOICES)
        }


class UserSelectForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False), label="Choose One User:", widget=forms.Select(
        attrs={'class':'user-select btn-block'}), empty_label="Choose One User...")
    class Meta:
        fields = ['users']
    

class UserForm(UserCreationForm):
    password1 = forms.CharField(label='', error_messages={'required': 'Enter the strong password.'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input--style-3', 'placeholder': 'Enter Your Password...'}))
    password2 = forms.CharField(label='', error_messages={'required': 'Password not matched.'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input--style-3', 'placeholder': 'Confirm Your Password...'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username' : TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Enter Your Username...'}),
            'email' : TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Enter Your Email...'}),
        }


class UserEditForm(forms.ModelForm):
    # username = forms.CharField(label='User Name',
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}))
    # email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username' : TextInput(attrs={'class': 'form-control', 'id': 'username'}),
            'email' : TextInput(attrs={'class': 'form-control', 'id': 'email'}),
        }


class UserProfileForm(forms.ModelForm):
    # profile_pic = forms.ImageField(label='Profile Picture')

    class Meta:
        model = UserProfile
        fields = ('profile_pic',)
        labels = {
            'profile_pic': "Profile Picture",
        }


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'input--style-3', 'placeholder': 'Your Old Password...'}))
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'input--style-3', 'placeholder': 'Enter Your New Password...'}))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'input--style-3', 'placeholder': 'Confirm Your New Password...'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        

class PasswordResetFormWithError(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'input--style-3', 'placeholder': 'Enter your e-mail to reset password.'}))

    class Meta:
        fields = ['email']
       
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = ("There is no user registered with the specified E-Mail address.")
            self.add_error('email', msg)
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(
                                 attrs={'class': 'input--style-3', 'placeholder': 'Enter Your New Password...'}))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(
                                    attrs={'class': 'input--style-3', 'placeholder': 'Confirm Your New Password...'}))
    class Meta:
        fields = ['new_password1', 'new_password2']