from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
import uuid
import asyncio
from authentication import models
import time

class BackupRestoreDBConfig():

    def back_up(self, user):
        channel_layer = get_channel_layer()
        try:
            token = uuid.uuid4()
            path = f'{settings.BASE_DIR}/bd/backup_{token}.json'
            data = dict(
                user=user,
                path=path
            )
            Session.objects.all().delete()
            models.BackupRestoreBD.objects.create(**data)
            with open(path, "w") as f:
                f.seek(0)
                call_command('dumpdata', indent=2,  stdout=f)
            asyncio.sleep(10)
            time.sleep(10)
            async_to_sync(channel_layer.group_send)(
                "events", {"type": "events.alarms",
                        "message": "Base de Datos Respaldada"})
        except Exception:
            async_to_sync(channel_layer.group_send)(
                "events", {"type": "events.alarms",
                        "message": "No se pudo respaldar la base de datos"})            
            

    def restore(self, pk):
        channel_layer = get_channel_layer()
        try:
            bd = get_object_or_404(models.BackupRestoreBD, pk=pk)
            path = bd.path
            call_command('flush', verbosity=0, interactive=False)
            call_command('loaddata', path, verbosity=0)
            time.sleep(10)
            Session.objects.all().delete()
            async_to_sync(channel_layer.group_send)(
                "events", {"type": "events.alarms",
                           "message": "Base de Datos Restaurada"})
        except Exception:
            async_to_sync(channel_layer.group_send)(
                "events", {"type": "events.alarms",
                           "message": "No se pudo restaurar la base de datos"})
