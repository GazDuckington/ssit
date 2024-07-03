from django.contrib import admin

from dana.models import Divisi, LogPengajuan, Metode, Nasabah, Pengajuan

# Register your models here.
admin.site.register(Nasabah)
admin.site.register(Divisi)
admin.site.register(Metode)
admin.site.register(Pengajuan)
admin.site.register(LogPengajuan)
