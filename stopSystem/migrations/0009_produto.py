# Generated by Django 4.2.6 on 2023-11-06 14:18

from django.db import migrations, models
import stopSystem.models


class Migration(migrations.Migration):

    dependencies = [
        ('stopSystem', '0008_remove_typelog_isrequiredstopreason_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto', stopSystem.models.UppercaseCharField(blank=True, max_length=15, null=True)),
                ('quantidade', models.IntegerField()),
            ],
        ),
    ]