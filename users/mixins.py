from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:photo_home")


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated  # 무조건 true를 return

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:photo_home")


class CreateStudioLimitView(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.has_studio is None:
            return True
        else:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:photo_home")


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
