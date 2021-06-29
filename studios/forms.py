from django import forms
from . import models


class SearchForm(forms.Form):
    search_name_address = forms.CharField(required=False, label="search!")


class CreateStudioForm(forms.ModelForm):
    class Meta:
        model = models.Studio
        fields = (
            "name",
            "studio_avatar",
            "phone_number",
            "kakao_chat",
            "address",
            "open_time",
            "close_time",
            "introduction",
            "using_info",
        )

    def save(self, *args, **kwargs):
        studio = super().save(commit=False)  # commit=False의 의미는 지금 당장 DB에 저장하지 않는다.
        return studio
