from django import forms

class LogRegForm(forms.Form):
    email = forms.EmailField(label='email',max_length=30)
    contra = forms.CharField(label='email', max_length=30)