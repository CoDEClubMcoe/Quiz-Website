from django import forms

class UserInfoForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
