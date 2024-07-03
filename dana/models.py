import uuid
from datetime import datetime
from django.contrib.auth.backends import UserModel
from django.db import models

from django.db.models.signals import post_save, post_init
from django.dispatch import receiver


class YesNo(models.IntegerChoices):
    YES = "1", "Yes"
    NO = "0", "No"


# Create your models here.
class Divisi(models.Model):
    class Meta:
        db_table = "m_divisi"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nama = models.CharField()
    is_del = models.SmallIntegerField(choices=YesNo.choices, default=YesNo.NO.value)

    def hard_delete(self):
        super(Divisi, self).delete()

    def delete(self, using=None, keep_parents=False):
        self.is_del = YesNo.YES.value
        self.save(update_fields=["is_del"])


class Nasabah(models.Model):
    class Meta:
        db_table = "m_nasabah"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nama = models.CharField()
    divisi = models.ForeignKey(Divisi, on_delete=models.CASCADE)
    uid = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_del = models.SmallIntegerField(choices=YesNo.choices, default=YesNo.NO.value)

    def hard_delete(self):
        super(Nasabah, self).delete()

    def delete(self, using=None, keep_parents=False):
        self.is_del = YesNo.YES.value
        self.save(update_fields=["is_del"])


class Metode(models.Model):
    class Meta:
        db_table = "m_metode"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nama = models.CharField()
    is_del = models.SmallIntegerField(choices=YesNo.choices, default=YesNo.NO.value)

    def hard_delete(self):
        super(Metode, self).delete()

    def delete(self, using=None, keep_parents=False):
        self.is_del = YesNo.YES.value
        self.save(update_fields=["is_del"])


class Pengajuan(models.Model):
    class Meta:
        db_table = "t_pengajuan"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nominal = models.FloatField()
    user = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    metode = models.ForeignKey(Metode, on_delete=models.CASCADE)
    is_del = models.SmallIntegerField(choices=YesNo.choices, default=YesNo.NO.value)

    def hard_delete(self):
        super(Pengajuan, self).delete()

    def delete(self, using=None, keep_parents=False):
        self.is_del = YesNo.YES.value
        self.save(update_fields=["is_del"])


class LogPengajuan(models.Model):
    class Meta:
        db_table = "t_log_pengajuan"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    pengajuan = models.ForeignKey(Pengajuan, on_delete=models.CASCADE)
    user = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    metode = models.ForeignKey(Metode, on_delete=models.CASCADE)
    nominal = models.FloatField()
    tanggal = models.DateTimeField(default=datetime.now())


# triggers
@receiver(post_init, sender=Pengajuan)
@receiver(post_save, sender=Pengajuan)
def create_log_pengajuan(sender, instance, **kwargs):
    LogPengajuan.objects.create(
        pengajuan=instance,
        user=instance.user,
        metode=instance.metode,
        nominal=instance.nominal,
    )
