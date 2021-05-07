from django import forms
from . import models


class SearchForm(forms.Form):
    search_name_address = forms.CharField(required=False,label="search!")
    
