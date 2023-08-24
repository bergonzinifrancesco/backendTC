# Generated by Django 4.2.4 on 2023-08-24 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('struttura', '0001_squashed_0004_alter_adminstruttura_admin_and_more'),
        ('chat', '0002_alter_message_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='struttura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='struttura.struttura'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
