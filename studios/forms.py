from django import forms
from . import models


class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    address = forms.CharField(required=False)
