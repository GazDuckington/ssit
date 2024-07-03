from django.contrib.auth.backends import UserModel
from django.db import models


# Create your models here.
class Divisi(models.Model):
    class Meta:
        db_table = "m_divisi"

    id = models.UUIDField(primary_key=True)
    nama = models.CharField()


class Nasabah(models.Model):
    class Meta:
        db_table = "m_nasabah"

    id = models.UUIDField(primary_key=True)
    nama = models.CharField()
    divis = models.ForeignKey(Divisi, on_delete=models.CASCADE)
    uid = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class Pengajuan(models.Model):
    class Meta:
        db_table = "m_pengajuan"

    id = models.UUIDField(primary_key=True)
    nominal = models.FloatField()
    user = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
