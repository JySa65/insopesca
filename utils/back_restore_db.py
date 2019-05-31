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
from datetime import datetime
import os

class BackupRestoreDBConfig():
    path = f'{settings.BASE_DIR}/bd'

    def back_up(self, user):
        channel_layer = get_channel_layer()
        try:
            token = uuid.uuid4()
            file = f'{self.path}/backup_{token}_{datetime.now()}.json'
            data = dict(
                user=user,
                path=file
            )
            models.BackupRestoreBD.objects.create(**data)
            Session.objects.all().delete()
            with open(file, "w") as f:
                f.seek(0)
                call_command('dumpdata', '--natural-foreign',
                             stdout=f)
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
            file = bd.path
            if not os.path.exists(file):
                async_to_sync(channel_layer.group_send)(
                    "events", {"type": "events.alarms",
                            "message": "Base De Datos no Existe en el servidor"})
                bd.delete()
                return False

            call_command('flush', verbosity=0, interactive=False)
            call_command('loaddata', file, verbosity=0)
            bd = models.BackupRestoreBD.objects.all()
            remove = []
            for i in os.listdir(self.path):
                for j in bd:
                    if f'{self.path}/{i}' != j.path:
                        remove.append(i)
            [os.remove(f'{self.path}/{i}') for i in remove]
            async_to_sync(channel_layer.group_send)(
                "events", {"type": "events.alarms",
                           "message": "Base de Datos Restaurada"})
            Session.objects.all().delete()
        except Exception as e:
            print(e)
            async_to_sync(channel_layer.group_send)(
                "events", {"type": "events.alarms",
                           "message": "No se pudo restaurar la base de datos"})
