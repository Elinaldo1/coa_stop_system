# Generated by Django 4.2.6 on 2023-10-30 19:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import stopSystem.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frente', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'vv_Frentes',
                'db_table': 'stop_system_NewView',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OnLogFleet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(blank=True, null=True)),
                ('description', stopSystem.models.UppercaseTextField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Última info da frota',
                'db_table': 'stop_system_onLogFleet',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', stopSystem.models.UppercaseCharField(max_length=30, unique=True, verbose_name='Categoria')),
            ],
            options={
                'verbose_name_plural': 'Categorias',
                'db_table': 'stop_system_categories',
            },
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fleet', models.PositiveIntegerField(unique=True, verbose_name='PX Frota')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(db_column='updated_at', default=django.utils.timezone.now, verbose_name='Atualização')),
                ('description', stopSystem.models.UppercaseTextField(null=True, verbose_name='Observação')),
                ('categoryId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.category', verbose_name='Categoria')),
            ],
            options={
                'verbose_name_plural': 'Frotas',
                'db_table': 'stop_system_fleets',
            },
        ),
        migrations.CreateModel(
            name='Front',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', stopSystem.models.UppercaseCharField(max_length=30, unique=True, verbose_name='Frente')),
            ],
            options={
                'verbose_name_plural': 'Frentes',
                'db_table': 'stop_system_fronts',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locationName', stopSystem.models.UppercaseCharField(max_length=100, unique=True, verbose_name='Fazenda')),
            ],
            options={
                'verbose_name_plural': 'Fazendas',
                'db_table': 'stop_system_locations',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', stopSystem.models.UppercaseCharField(max_length=30, unique=True, verbose_name='Operação')),
            ],
            options={
                'verbose_name_plural': 'Operações',
                'db_table': 'stop_system_operations',
            },
        ),
        migrations.CreateModel(
            name='StatusFleet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', stopSystem.models.UppercaseCharField(max_length=15, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Status da Frota',
                'db_table': 'stop_system_status_fleet',
            },
        ),
        migrations.CreateModel(
            name='StopGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', stopSystem.models.UppercaseCharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Grupos de parada',
                'db_table': 'stop_system_stop_groups',
            },
        ),
        migrations.CreateModel(
            name='TypeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', stopSystem.models.UppercaseCharField(max_length=11, unique=True, verbose_name='Tipo')),
            ],
            options={
                'verbose_name_plural': 'Tipos de Log da Frota',
                'db_table': 'stop_system_type_logs',
            },
        ),
        migrations.CreateModel(
            name='StopReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', stopSystem.models.UppercaseCharField(max_length=30, verbose_name='Motivo')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.stopgroup', verbose_name='Grupo')),
            ],
            options={
                'verbose_name_plural': 'Motivos de parada',
                'db_table': 'stop_system_stop_reasons',
            },
        ),
        migrations.CreateModel(
            name='LogAgricola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(db_column='created_at', default=django.utils.timezone.now, verbose_name='Dt_início')),
                ('updatedAt', models.DateTimeField(blank=True, db_column='updated_at', null=True, verbose_name='Dt_fim')),
                ('description', stopSystem.models.UppercaseTextField(null=True, verbose_name='Observação')),
                ('categoryId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.category', verbose_name='Categoria')),
                ('fleetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.fleet', verbose_name='Frota')),
                ('frontId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.front', verbose_name='Frente')),
                ('locationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.location', verbose_name='Fazenda')),
                ('operationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.operation', verbose_name='Operação')),
                ('stopReasonId', models.ForeignKey(db_column='stop_reason_id', on_delete=django.db.models.deletion.CASCADE, to='stopSystem.stopreason', verbose_name='Motivo Parada')),
                ('typeLogId', models.ForeignKey(db_column='type_log_id', on_delete=django.db.models.deletion.CASCADE, to='stopSystem.typelog', verbose_name='Tipo de Log')),
            ],
            options={
                'verbose_name_plural': 'Logs(Histórico)',
                'db_table': 'stop_system_logs_agricolas',
            },
        ),
        migrations.AddField(
            model_name='fleet',
            name='frontId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.front', verbose_name='Frente'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='locationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.location', verbose_name='Fazenda'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='operationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.operation', verbose_name='Operação'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='statusId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stopSystem.statusfleet', verbose_name='Status da Frota'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='stopReasonId',
            field=models.ForeignKey(db_column='stop_reason_id', on_delete=django.db.models.deletion.CASCADE, to='stopSystem.stopreason', verbose_name='Motivo Parada'),
        ),
    ]
