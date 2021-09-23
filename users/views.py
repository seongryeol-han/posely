import os
import requests
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, render
from django.contrib.auth import authenticate, login, logout
from . import forms, models, mixins
from django.core.files.base import ContentFile
from django.contrib.auth.forms import User
from users import mixins as user_mixins

# Create your views here.


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    # success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):  # 유저가 가려고 했던 그 주소로 다시 돌려준다.
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:photo_home")


def log_out(request):
    logout(request)
    return redirect(reverse("core:photo_home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:photo_home")

    def form_valid(
        self, form
    ):  # (form이 유효하다면 form.save()를 실행시킨다.)인증해서 로그인 시킨다. 회원가입하면 바로 로그인되게 하는거구나.
        form.save()  # form 을 save 한다.
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# 카카오 파트 05.09
def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    print("@@@@@@@@@@@")
    print(client_id)
    print("@@@@@@@@@@@")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        print(client_id)
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        print("@@@@@@@@@@@@@@@")
        print(profile_json)
        print("@@@@@@@@@@@@@@@")
        email = profile_json.get("kakao_account").get("email")
        if email is None:
            raise KakaoException()
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGING_KAKAO:
                raise KakaoException()
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGING_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        login(request, user)
        return redirect(reverse("core:photo_home"))
    except KakaoException:
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"
    template_name = "users/user_profile.html"


class EditProfileView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.User
    template_name = "users/user_edit.html"
    fields = (
        "nickname",
        "phone_number",
        "avatar",
        "petname",
        "bio",
    )

    def get_object(self, queryset=None):  # 룸 호스트랑 요청하는 사람이랑 같은지
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["phone_number"].widget.attrs = {"placeholder": "- 제외"}

        form.fields["nickname"].label = "닉네임"
        form.fields["phone_number"].label = "전화번호"
        form.fields["avatar"].label = "내 반려동물 사진"
        form.fields["petname"].label = "내 반려동물 이름"
        form.fields["bio"].label = "내 반려동물에게 하고 싶은 말"
        return form
