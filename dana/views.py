from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .services import ServiceLogPengajuan, ServicePengajuan


# Create your views here.
class HelloView(View):
    def get(self, request):
        context = {"message": "hello", "user": request.user}
        return render(request, "hello.html", context)


class Pengajuan(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    service = ServicePengajuan()
    log_service = ServiceLogPengajuan()

    def get(self, request):
        try:
            user = request.user
            logs, err = self.log_service.filter_log_pengajuan(user=user)
            if err is not None:
                context = {
                    "status": False,
                    "message": f"something went wrong: {err}",
                    "data": [],
                }
            context = {"status": True, "message": "success", "data": logs}
            return render(request, "pengajuan/logs.html", context)
        except Exception as e:
            raise e

    def post(self, request): ...
    def put(self, request): ...
    def delete(self, request): ...
