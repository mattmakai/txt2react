import random, string

from django import forms
from django.contrib.auth.models import User

from payments.models import Customer
from .models import ReactionEvent

class ReactionEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReactionEventForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ReactionEvent
        fields = ['name', 'url', 'event_date',]


class LoginForm(forms.Form):
    login_email = forms.CharField(max_length=75)
    login_password = forms.CharField(max_length=25, widget=forms.PasswordInput,
        label="Password")


class EmailSignUpForm(forms.Form):
    first_name = forms.CharField(max_length=75, 
        widget=forms.TextInput(attrs={'class':'span3'}))
    email = forms.CharField(max_length=75,
        widget=forms.TextInput(attrs={'class':'span3'}))
    password = forms.CharField(max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'span3'}))
   
    def create_email_user(self):
        pw = self.cleaned_data['password']
        new_user = User.objects.create_user(self.cleaned_data['email'],
            self.cleaned_data['email'], pw)
        new_user.first_name = self.cleaned_data['first_name']
        new_user.save()
        c = Customer()
        c.user = new_user
        c.preferred_name = self.cleaned_data['first_name']
        c.save()
        return c, pw

