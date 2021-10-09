from django import forms
from . import models

class SalonSearchForm(forms.Form):
    salon_search = forms.CharField(required=False, label="search!")

