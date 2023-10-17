from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList

class LogRegForm(forms.Form):
    email = forms.EmailField(label='email',max_length=30)
    contra = forms.CharField(label='contra', max_length=30)

class UpdateForm(forms.Form):
    def __init__(self, data: Mapping[str, Any]) -> None:
        data = dict(data)
        data['isScan'] = bool(int(data['isScan'][0]))
        data['NBA'] = int(data['NBA'][0])
        data['CA'] = int(data['CA'][0])
        data['CR'] = int(data['CR'][0])
        data['userID'] = int(data['userID'][0])
        data['email'] = data['email'][0]
        super().__init__(data)

    def clean(self):
        return self.data

    isScan = forms.BooleanField(label='isScan')
    email = forms.EmailField(label='email')
    userID = forms.IntegerField(label='userID')
    NBA = forms.IntegerField(label='NBA')
    CA = forms.IntegerField(label='CA')
    CR = forms.IntegerField(label='CR')