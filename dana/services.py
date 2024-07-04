from typing import Optional, Tuple, Union
import uuid

from django.db.models.query import QuerySet
from dana.models import Action, LogPengajuan, Metode, Nasabah, Pengajuan, YesNo


class ServiceLogPengajuan:
    def get_log_pengajuan(self, **kwargs):
        try:
            user = kwargs.get("user", None)
            if user is not None and isinstance(user, str):
                kwargs["user"] = uuid.UUID(user)
            id = kwargs.get("id", None)
            if id is not None and isinstance(id, str):
                kwargs["id"] = uuid.UUID(id)
            pengajuan = LogPengajuan.objects.get(kwargs)
            return pengajuan, None
        except LogPengajuan.DoesNotExist:
            return {}, None
        except Exception as e:
            return None, f"error getting log pengajuan: {e}"

    def create_log_pengajuan(self, **kwargs):
        try:
            logs = LogPengajuan.objects.create(**kwargs)
            print("new_logs: ", logs)
            return None
        except Exception as e:
            raise e

    def filter_log_pengajuan(self, **kwargs):
        try:
            id = kwargs.get("id", None)
            if id is not None and isinstance(id, str):
                kwargs["id"] = uuid.UUID(id)

            pengajuan = LogPengajuan.objects.filter(**kwargs)
            print(kwargs, pengajuan.query)
            return pengajuan, None
        except LogPengajuan.DoesNotExist:
            return [], None
        except Exception as e:
            return None, f"error getting log pengajuan: {e}"


class ServicePengajuan:
    log_service = ServiceLogPengajuan()

    def get_pengajuan(self, **kwargs) -> Tuple[Optional[Pengajuan], Optional[str]]:
        try:
            id = kwargs.get("id", None)
            if id is not None and isinstance(id, str):
                kwargs["id"] = uuid.UUID(id)
            pengajuan = Pengajuan.objects.get(**kwargs, is_del=YesNo.NO.value)
            return pengajuan, None
        except Pengajuan.DoesNotExist:
            return None, "pengajuan does not exists"
        except Exception as e:
            return None, f"error getting pengajuan: {e}"

    def filter_pengajuan(self, **kwargs) -> Tuple[Optional[QuerySet], Optional[str]]:
        try:
            id = kwargs.get("id", None)
            if id is not None and isinstance(id, str):
                kwargs["id"] = uuid.UUID(id)
            pengajuan = Pengajuan.objects.filter(**kwargs, is_del=YesNo.NO.value)
            return pengajuan, None
        except Pengajuan.DoesNotExist:
            return None, "pengajuan does not exists"
        except Exception as e:
            return None, f"error getting pengajuan: {e}"

    def create_pengajuan(self, **kwargs):
        try:
            new_pengajuan = Pengajuan.objects.create(**kwargs)

            log = {
                "pengajuan": new_pengajuan,
                "metode": new_pengajuan.metode,
                "nominal": new_pengajuan.nominal,
                "user": new_pengajuan.user,
            }
            err = self.log_service.create_log_pengajuan(**log)
            if err is not None:
                print(f"error creating log: {err}")
            return new_pengajuan, None
        except Exception as e:
            return None, f"Error creating pengajuan: {e}"

    def update_pengajuan(
        self, pengajuan: Pengajuan, **kwargs
    ) -> Tuple[Optional[Pengajuan], Optional[str]]:
        try:
            if pengajuan is None:
                return None, "pengajuan not found"

            mid = kwargs.get("metode", pengajuan.metode.id)
            pengajuan.metode = Metode.objects.get(id=mid)
            pengajuan.nominal = kwargs.get("nominal", pengajuan.nominal)
            pengajuan.user = kwargs.get("user", pengajuan.user)
            pengajuan.save()
            print("saved")
            return pengajuan, None
        except Exception as e:
            raise e
            # return None, f"error updating pengajuan: {e}"

    def delete_pengajuan(self, id):
        try:
            id_uuid = uuid.UUID(id)
            pengajuan, err = self.get_pengajuan(id=id_uuid)
            if err is not None:
                return err
            if pengajuan:
                if pengajuan.is_del == YesNo.YES.value:
                    return False, f"{id} already deleted"
                pengajuan.delete()
                return True, None
            else:
                return False, None
        except Exception as e:
            return False, f"Error deleting pengajuan: {e}"
