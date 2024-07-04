from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from dana.forms import PengajuanForm
from dana.models import Action, Metode, Nasabah, YesNo
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
            form = PengajuanForm(user=user)
            nasabah = Nasabah.objects.get(uid=user)
            metode = Metode.objects.filter(is_del=YesNo.NO.value)
            pngjn, errp = self.service.filter_pengajuan(user=nasabah)
            logs, err = self.log_service.filter_log_pengajuan(user=nasabah)
            if err is not None:
                context = {
                    "status": False,
                    "message": f"something went wrong: {err}",
                    "data": [],
                    "form": form,
                }
            if errp is not None:
                context = {
                    "status": False,
                    "message": f"something went wrong: {errp}",
                    "data": [],
                    "form": form,
                }
            context = {
                "status": True,
                "message": "success",
                "data": logs,
                "pengajuan": pngjn,
                "form": form,
                "metodes": metode,
            }
            return render(request, "pengajuan/logs.html", context)
        except Exception as e:
            context = {
                "status": False,
                "message": f"something went wrong: {e}",
                "data": [],
                "form": PengajuanForm(),
            }
            return render(request, "pengajuan/logs.html", context)

    def post(self, request):
        try:
            form = PengajuanForm(request.POST, user=request.user)
            if not form.is_valid():
                context = {"status": False, "message": form.errors, "data": None}
            new_pengajuan, err = self.service.create_pengajuan(**form.cleaned_data)
            if err is not None:
                context = {"status": False, "message": "error", "data": err}
            context = {"status": True, "message": "success", "data": new_pengajuan}
            print(f"create: {context}")
            return redirect("pengajuan")
        except Exception as e:
            raise e


class UpdatePengajuan(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    service = ServicePengajuan()
    log_service = ServiceLogPengajuan()

    def post(self, request, id):
        try:
            pengajuan, err = self.service.get_pengajuan(id=id)
            if err is not None:
                context = {"status": False, "message": err, "data": {}}

            if pengajuan is None:
                context = {"status": False, "message": "pengajuan is empty"}
                return JsonResponse(context, status=400)

            kwargs = {
                "nominal": request.POST.get("nominal", pengajuan.nominal),
                "metode": request.POST.get("metode", pengajuan.metode.id),
                "user": Nasabah.objects.get(uid=request.user),
            }
            print("new data", kwargs)
            if pengajuan is not None:
                updated_pengajuan, err = self.service.update_pengajuan(
                    pengajuan, **kwargs
                )
                if err is not None:
                    context = {"status": False, "message": err}

                context = {
                    "status": True,
                    "message": "success",
                    "data": updated_pengajuan,
                }

                if updated_pengajuan:
                    log = {
                        "pengajuan": updated_pengajuan,
                        "metode": updated_pengajuan.metode,
                        "nominal": updated_pengajuan.nominal,
                        "user": updated_pengajuan.user,
                        "action": Action.UPDATE.value,
                    }
                    err = self.log_service.create_log_pengajuan(**log)
                    if err is not None:
                        print(f"error creating log: {err}")
            else:
                context = {"status": False, "message": "pengajuan is empty"}
            print(f"update: {id}", context)
            return redirect("pengajuan")
        except Exception as e:
            raise e


class DeletePengajuan(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    service = ServicePengajuan()
    log_service = ServiceLogPengajuan()

    def post(self, request, id):
        try:
            pengajuan, err = self.service.get_pengajuan(id=id)
            if err is not None:
                context = {"status": False, "message": err, "data": {}}

            if pengajuan is None:
                context = {"status": False, "message": "pengajuan is empty"}
                return JsonResponse(context, status=400)

            if pengajuan is not None:
                deleted_pengajuan, err = self.service.delete_pengajuan(pengajuan)
                if err is not None:
                    context = {"status": False, "message": err}
                if deleted_pengajuan is False:
                    context = {
                        "status": False,
                        "message": f"failed to delete pengajuan {pengajuan.id}",
                    }

                context = {
                    "status": True,
                    "message": "success",
                }

                if pengajuan:
                    log = {
                        "pengajuan": pengajuan,
                        "metode": pengajuan.metode,
                        "nominal": pengajuan.nominal,
                        "user": pengajuan.user,
                        "action": Action.DELETE.value,
                    }
                    err = self.log_service.create_log_pengajuan(**log)
                    if err is not None:
                        print(f"error creating log: {err}")
            else:
                context = {"status": False, "message": "pengajuan is empty"}
            print(f"delete: {context}")
            return redirect("pengajuan")
        except Exception as e:
            raise e
