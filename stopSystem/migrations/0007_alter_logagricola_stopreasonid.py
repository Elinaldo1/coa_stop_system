# Generated by Django 4.2.6 on 2023-11-01 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stopSystem', '0006_alter_fleet_stopreasonid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logagricola',
            name='stopReasonId',
            field=models.ForeignKey(blank=True, db_column='stop_reason_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='stopSystem.stopreason', verbose_name='Motivo Parada'),
        ),
    ]
