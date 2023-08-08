# Generated by Django 4.2.3 on 2023-08-08 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('struttura', '0014_delete_prenotazione'),
        ('prenotazione', '0005_alter_prenotazione_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prenotazione',
            name='struttura',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='struttura.struttura'),
            preserve_default=False,
        ),
    ]
