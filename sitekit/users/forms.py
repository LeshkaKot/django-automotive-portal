from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from prompt_toolkit.validation import ValidationError



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Login",
                               widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput(attrs={"class": "form-input"}))


    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        labels = {'email': 'E-mail', 'first_name': 'Name/Nickname', }
        widgets = {'email': forms.TextInput(attrs={"class": "form-input"}),
                   'first_name': forms.TextInput(attrs={"class": "form-input"})}


    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Login",
                               widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.CharField(disabled=True, required=False, label="E-mail",
                               widget=forms.TextInput(attrs={"class": "form-input"}))
    this_year = datetime.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100,this_year-5))))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'date_birth', 'first_name']
        labels = {'first_name': 'Name/Nickname'}
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-input"})
        }



class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Password confirmation",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

