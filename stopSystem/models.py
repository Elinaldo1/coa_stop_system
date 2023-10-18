from django.db import models, IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Fleet(models.Model):
    fleet = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name_plural = 'Frotas'

    def __str__(self):
        return str(self.fleet)

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

class StatusFleet(models.Model):
    status = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Status da Frota'

    def __str__(self):
        return self.status

class Location(models.Model):
    location = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural =  'Fazendas'


    def __str__(self):
        return self.location


class Operation(models.Model):
    operation = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Operações'

    def __str__(self):
        return self.operation

class OperationFront(models.Model):
    name = models.CharField(max_length=30)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Frentes'

    def __str__(self):
        return self.name

class StopGroup(models.Model):
    group = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Grupos de parada'

    def __str__(self):
        return self.group

class StopReason(models.Model):
    reason = models.CharField(max_length=30)
    group = models.ForeignKey(StopGroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Motivos de parada'

    def __str__(self):
        return self.reason

class LogAgricola(models.Model):

    fleetId = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(StatusFleet, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    stopReason = models.ForeignKey(StopReason, on_delete=models.CASCADE)
    operationFront = models.ForeignKey(OperationFront, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Logs'

    def __str__(self):
        return str(self.id)
    
class OnLogFleet(models.Model):

    fleetId = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(StatusFleet, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    stopReason = models.ForeignKey(StopReason, on_delete=models.CASCADE)
    operationFront = models.ForeignKey(OperationFront, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Última info da frota'
        managed = False
        db_table = 'onLogFleet'

    def __str__(self):
        return str(self.stopReason.reason)
    
class NewView(models.Model):
    # codigo = models.IntegerField()
    frente = models.CharField(max_length=255)
    # localizacao = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Visualizar view'
        managed = False
        db_table = 'NewView'
        # NewView = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)
