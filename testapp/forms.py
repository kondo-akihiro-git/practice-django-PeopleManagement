from django import forms
from .models import UserInfo

class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ["user_name","company_name","mail_address","password","test_empty","picture","slug" ]

class UserForm_add(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ["user_name","company_name","mail_address","password","picture","test_empty","slug" ]

class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()