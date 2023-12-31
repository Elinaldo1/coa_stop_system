# Generated by Django 4.2.6 on 2023-11-01 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stopSystem', '0005_typelog_isrequiredstopreason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fleet',
            name='stopReasonId',
            field=models.ForeignKey(blank=True, db_column='stop_reason_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='stopSystem.stopreason', verbose_name='Motivo Parada'),
        ),
        migrations.AlterField(
            model_name='typelog',
            name='isRequiredStopReason',
            field=models.BooleanField(db_column='is_requiered_stop_reason', default=True, verbose_name='Informar Motivo de Parada'),
        ),
    ]
