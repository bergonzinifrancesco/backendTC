# Generated by Django 4.2.4 on 2023-08-15 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('struttura', '0003_alter_adminstruttura_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminstruttura',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='adminstruttura',
            name='struttura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='struttura.struttura'),
        ),
    ]
