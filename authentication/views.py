from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.urls import reverse_lazy
from django.views import View
from ssit.forms import LoginForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                User = get_user_model()
                if User.objects.filter(pk=user.pk, is_superuser=True).exists():
                    return redirect("admin:index")
                else:
                    return redirect("greet-dana")
        return render(request, "auth/login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy("login"))
