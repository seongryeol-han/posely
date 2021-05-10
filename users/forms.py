from django import forms
from django.contrib.auth import password_validation
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"type": "email", "placeholder": ("이메일 주소")}),
        label="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"}), label=""
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data

            else:
                self.add_error("passwod", forms.ValidationError("비밀번호가 틀렸습니다."))

        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("사용자가 존재하지 않습니다."))


class SignUpForm(forms.ModelForm):  # model에 채우는 폼, uniqueness를 검증한다.
    class Meta:
        model = models.User
        fields = ("email", "first_name", "phone_number")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "email": forms.EmailInput(attrs={"placeholder": "이메일"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "휴대폰 번호"}),
        }
        labels = {"first_name": "", "email": "", "phone_number": ""}

    # password는 따로 적어줘야함. 암호화 되어있기 때문에. 그리고 model에 없으니까.
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"}), label=""
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"}), label=""
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(email=email)
            self.add_error(
                "email", forms.ValidationError("이미 가입된 이메일입니다. 다른 이메일을 입력해 주세요.")
            )

        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("확인 비밀번호가 일치하지 않습니다.")
        else:
            return password

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password1", error)

    # model에서 username에 email 넣고 password 저장하고
    def save(self, *args, **kwargs):
        user = super().save(
            commit=False
        )  # (아직 데이터베이스에 올릴필요없으니까)commit=False란 의미는, 장고 object에는 데이터가 올라가는데 데이터베이스에는 올라가지 않게 하는것임.
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)  # 비번 암호화
        user.save()  # 여기서는 commit=True가 포함.
