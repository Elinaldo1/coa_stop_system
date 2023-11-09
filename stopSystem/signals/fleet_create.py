from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .. import models

# Create your views here.


class FleetSignals:
    @staticmethod
    @receiver(pre_save, sender=models.Fleet)
    def set_is_new_flag(sender, instance, **kwargs):
        if instance.pk:
            print(
                f"Vou Atualizar uma frota========================================={instance.description}"
            )
            instance.is_new_fleet = False
        else:
            print(f"Vou Salvar/criar uma frota====={instance.description}")
            instance.is_new_fleet = True

    @staticmethod
    @receiver(post_save, sender=models.Fleet)
    def create_log(sender, instance, **kwargs):
        if instance.is_new_fleet:
            # tratativa quando criar uma nova frota

            print(
                f"Criando o LOG da nova frota========================================={instance.description}"
            )

            models.LogAgricola.objects.create(
                fleetId=instance,
                categoryId=instance.categoryId,
                # createdAt=instance.createdAt, #default now
                updatedAt=instance.updatedAt,
                typeLogId=instance.statusId.typeLog,  # conforme o status(instance.status)
                description=instance.description,
                stopReasonId=instance.stopReasonId,
                operationId=instance.operationId,
                frontId=instance.frontId,
                locationId=instance.locationId,
            )
            # self.message_user(request, "Registros de LogAgricola criados com sucesso.")
        else:
            print(f"Atualizei o frota====={instance.is_new_fleet}")
            # tratativa quando atualizar uma frota
            # identifique os campos alterados
            # com base nas aterações atualize um log ou crie um novo
            # defina quais alter irão gerar log de notificação automático
