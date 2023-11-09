from django import forms
from django.db import models, IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


from django.db import models


class UppercaseCharField(models.CharField):
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
        return value


class UppercaseTextField(models.TextField):
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
        return value


# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     date = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title


class Category(models.Model):
    name = UppercaseCharField(max_length=30, unique=True, verbose_name="Categoria")

    class Meta:
        verbose_name_plural = "Categorias"
        db_table = "stop_system_categories"

    def __str__(self):
        return self.name


class TypeLog(models.Model):
    type = UppercaseCharField(max_length=11, unique=True, verbose_name="Tipo")
    isStop = models.BooleanField(
        db_column="is_stop", default=True, verbose_name="Exige Parada?"
    )

    class Meta:
        verbose_name_plural = "Tipos de Log da Frota"
        db_table = "stop_system_type_logs"

    def __str__(self) -> str:
        return self.type


# situação atual da frota
class StatusFleet(models.Model):
    status = UppercaseCharField(max_length=15, unique=True)
    typeLog = models.ForeignKey(
        TypeLog, verbose_name="Tipo de Log", on_delete=models.CASCADE, default=0
    )
    isRequiredStopReason = models.BooleanField(
        default=True,
        verbose_name="Informar Motivo de Parada",
        db_column="is_requiered_stop_reason",
    )

    class Meta:
        verbose_name_plural = "Status da Frota"
        db_table = "stop_system_status_fleet"

    def __str__(self):
        return self.status


class Location(models.Model):
    locationName = UppercaseCharField(
        max_length=100, unique=True, verbose_name="Fazenda"
    )

    class Meta:
        verbose_name_plural = "Fazendas"
        db_table = "stop_system_locations"

    def __str__(self):
        return self.locationName


class Operation(models.Model):
    operation = UppercaseCharField(max_length=30, unique=True, verbose_name="Operação")

    class Meta:
        verbose_name_plural = "Operações"
        db_table = "stop_system_operations"

    def __str__(self):
        return self.operation


class Front(models.Model):
    name = UppercaseCharField(max_length=30, unique=True, verbose_name="Frente")

    class Meta:
        verbose_name_plural = "Frentes"
        db_table = "stop_system_fronts"

    def __str__(self):
        return self.name


class StopGroup(models.Model):
    group = UppercaseCharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = "Grupos de parada"
        db_table = "stop_system_stop_groups"

    def __str__(self):
        return self.group


class StopReason(models.Model):
    reason = UppercaseCharField(max_length=30, verbose_name="Motivo")
    group = models.ForeignKey(StopGroup, on_delete=models.CASCADE, verbose_name="Grupo")

    class Meta:
        verbose_name_plural = "Motivos de parada"
        db_table = "stop_system_stop_reasons"

    def __str__(self):
        return self.reason


class Fleet(models.Model):
    fleet = models.PositiveIntegerField(unique=True, verbose_name="PX Frota")
    categoryId = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoria"
    )
    createdAt = models.DateTimeField(default=timezone.now)  # não editavel
    updatedAt = models.DateTimeField(
        default=timezone.now, db_column="updated_at", verbose_name="Última Atualização"
    )
    statusId = models.ForeignKey(
        StatusFleet, on_delete=models.CASCADE, verbose_name="Status da Frota"
    )
    description = UppercaseTextField(null=True, blank=True, verbose_name="Observação")
    stopReasonId = models.ForeignKey(
        StopReason,
        db_column="stop_reason_id",
        on_delete=models.CASCADE,
        verbose_name="Motivo Parada/Notificação",
        null=True,
        blank=True,
    )
    operationId = models.ForeignKey(
        Operation, on_delete=models.CASCADE, verbose_name="Operação"
    )
    frontId = models.ForeignKey(Front, on_delete=models.CASCADE, verbose_name="Frente")
    locationId = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="Fazenda"
    )

    class Meta:
        verbose_name_plural = "Frotas"
        db_table = "stop_system_fleets"

    # def clean(self):
    #     print(
    #         f"======================kkkkk==={self.statusId.typeLog.isRequiredStopReason}"
    #     )
    #     print(self.stopReasonId)
    #     if self.statusId.typeLog.isRequiredStopReason:
    #         if not self.stopReasonId:
    #             raise ValidationError(
    #                 "O campo 'Motivo de Parada' é obrigatório quando 'statusId.typeLog.isRequiredStopReason' é verdadeiro."
    #             )

    def __str__(self):
        return str(self.fleet)


class LogAgricola(models.Model):
    fleetId = models.ForeignKey(Fleet, on_delete=models.CASCADE, verbose_name="Frota")
    categoryId = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoria"
    )
    createdAt = models.DateTimeField(
        default=timezone.now, db_column="created_at", verbose_name="Dt_início"
    )
    updatedAt = models.DateTimeField(
        blank=True, null=True, db_column="updated_at", verbose_name="Dt_fim"
    )  # dtultimocontato
    typeLogId = models.ForeignKey(
        TypeLog,
        db_column="type_log_id",
        on_delete=models.CASCADE,
        verbose_name="Tipo de Log",
    )
    description = UppercaseTextField(null=True, blank=True, verbose_name="Observação")
    stopReasonId = models.ForeignKey(
        StopReason,
        null=True,
        blank=True,
        db_column="stop_reason_id",
        on_delete=models.CASCADE,
        verbose_name="Motivo Parada",
    )
    operationId = models.ForeignKey(
        Operation, on_delete=models.CASCADE, verbose_name="Operação"
    )
    frontId = models.ForeignKey(Front, on_delete=models.CASCADE, verbose_name="Frente")
    locationId = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="Fazenda"
    )

    class Meta:
        verbose_name_plural = "Logs(Histórico)"
        db_table = "stop_system_logs_agricolas"

    def __str__(self):
        return str(self.id)


# class OnLogFleet(models.Model):

#     fleetId = models.ForeignKey(Fleet, on_delete=models.CASCADE)
#     category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
#     createdAt = models.DateTimeField(default=timezone.now)
#     updatedAt = models.DateTimeField(blank=True, null=True)
#     status = models.ForeignKey(StatusFleet, on_delete=models.CASCADE)
#     description = UppercaseTextField(null=True)
#     stopReason = models.ForeignKey(StopReason, on_delete=models.CASCADE)
#     # operationFront = models.ForeignKey(OperationFront, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = 'Última info da frota'
#         managed = False
#         db_table = 'stop_system_onLogFleet'

#     def __str__(self):
#         return str(self.stopReason.reason)


class NewView(models.Model):
    # codigo = models.IntegerField()
    frente = models.CharField(max_length=255)
    # localizacao = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "vv_Frentes"
        managed = False
        db_table = "stop_system_NewView"
        # NewView = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)


class Produto(models.Model):
    produto = UppercaseCharField(null=True, blank=True, max_length=15)
    quantidade = models.IntegerField()

    def __str__(self):
        return str(self.quantidade)
