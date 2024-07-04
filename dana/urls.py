from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.HelloView.as_view(), name="greet-dana"),
    path("pengajuan/", views.Pengajuan.as_view(), name="pengajuan"),
    path(
        "pengajuan/<uuid:id>/", views.UpdatePengajuan.as_view(), name="pengajuan_update"
    ),
]
