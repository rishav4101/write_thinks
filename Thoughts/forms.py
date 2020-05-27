from django import forms
from .models import thots, Relates, Profile, Likes
from django.forms import ModelForm
from allauth.account.forms import SignupForm


class ThoughtForm(ModelForm):
    class Meta:
        model = thots
        fields = ['head', 'thought']


class RelateForm(ModelForm):
    class Meta:
        model = Relates
        fields = ['relating']


class AboutForm(forms.Form):
    about_field = forms.CharField(max_length=2000)


class LikeForm(ModelForm):
    class Meta:
        model = Likes
        fields = ['liked']
# class LikeForm(forms.Form):
#     btn = forms.CharField()


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
