# Generated by Django 4.2.3 on 2023-08-01 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('struttura', '0009_adminstruttura_id_alter_adminstruttura_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminstruttura',
            name='id',
        ),
        migrations.AlterField(
            model_name='adminstruttura',
            name='struttura',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='struttura.struttura'),
        ),
    ]
