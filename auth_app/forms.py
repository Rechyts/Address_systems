from django import forms
from blog_app.models import UserProfile


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    birthday = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'orgname', 'birthday']
