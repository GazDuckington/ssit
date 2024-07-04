import uuid
from django.core.management.base import BaseCommand
from decouple import config
from django.db import connection
from dana.models import Divisi


class Command(BaseCommand):
    help = "Create a superuser if it does not exist"

    def handle(self, *args, **kwargs):
        try:
            divis_query = f"""
    INSERT INTO public.m_divisi (id,nama,is_del) VALUES
     ('{uuid.uuid4()}','Operational & Procurement',0),
     ('{uuid.uuid4()}','HC & GA',0),
     ('{uuid.uuid4()}','Marketing & Sales',0),
     ('{uuid.uuid4()}','Finance Accounting & Tax',0);
        """
            mtd_query = f"""
    INSERT INTO public.m_metode (id,nama,is_del) VALUES
     ('{uuid.uuid4()}','Cash',0),
     ('{uuid.uuid4()}','Transfer',0),
     ('{uuid.uuid4()}','Auto Debit',0),
     ('{uuid.uuid4()}','Lain-lain',0);
                """
            with connection.cursor() as cursor:
                cursor.execute(divis_query)
                cursor.execute(mtd_query)

            self.stdout.write(
                self.style.SUCCESS("Successfully init divisi & metode data")
            )
        except Exception as e:
            raise e
