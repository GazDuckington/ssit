import uuid
from dana.models import LogPengajuan, Pengajuan, YesNo


class ServicePengajuan:
    def get_pengajuan(self, **kwargs):
        try:
            id = kwargs.get("id", None)
            if id is not None and isinstance(id, str):
                kwargs["id"] = uuid.UUID(id)
            pengajuan = Pengajuan.objects.get(kwargs, is_del=YesNo.NO.value)
            return pengajuan, None
        except Pengajuan.DoesNotExist:
            return {}, None
        except Exception as e:
            return None, f"error getting pengajuan: {e}"

    def create_pengajuan(self, **kwargs):
        try:
            new_pengajuan = Pengajuan.objects.create(**kwargs)
            return new_pengajuan, None
        except Exception as e:
            return None, f"Error creating pengajuan: {e}"

    def update_pengajuan(self, id, **kwargs):
        try:
            id_uuid = uuid.UUID(id)
            pengajuan, err = self.get_pengajuan(id=id_uuid)
            if pengajuan is None:
                return None
            if err is not None:
                return err

            for k, v in kwargs.items():
                if hasattr(pengajuan, k):
                    setattr(pengajuan, k, v)
                pengajuan.save()
                return pengajuan, None
        except Exception as e:
            return None, f"error updating pengajuan: {e}"

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


class ServiceLogPengajuan:
    def get_log_pengajuan(self, **kwargs):
        try:
            id = kwargs.get("id", None)
            if id is not None and isinstance(id, str):
                kwargs["id"] = uuid.UUID(id)
            pengajuan = LogPengajuan.objects.get(kwargs)
            return pengajuan, None
        except LogPengajuan.DoesNotExist:
            return {}, None
        except Exception as e:
            return None, f"error getting log pengajuan: {e}"

    def filter_log_pengajuan(self, **kwargs):
        try:
            id = kwargs.get("id", None)
            if id is not None and isinstance(id, str):
                kwargs["id"] = uuid.UUID(id)
            pengajuan = LogPengajuan.objects.filter(kwargs)
            return pengajuan, None
        except LogPengajuan.DoesNotExist:
            return [], None
        except Exception as e:
            return None, f"error getting log pengajuan: {e}"
