# Generated by Django 4.2.3 on 2023-07-26 15:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import userInfo.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaratteristicheGioco',
            fields=[
                ('car_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('principale', models.CharField(choices=[('veloce', 'Veloce'), ('agile', 'Agile'), ('tecnico', 'Tecnico'), ('fisico', 'Fisico'), ('tattico', 'Tattico'), ('acrobata', 'Acrobata')], max_length=8)),
                ('secondaria', models.CharField(blank=True, choices=[('veloce', 'Veloce'), ('agile', 'Agile'), ('tecnico', 'Tecnico'), ('fisico', 'Fisico'), ('tattico', 'Tattico'), ('acrobata', 'Acrobata')], max_length=8)),
                ('terziaria', models.CharField(blank=True, choices=[('veloce', 'Veloce'), ('agile', 'Agile'), ('tecnico', 'Tecnico'), ('fisico', 'Fisico'), ('tattico', 'Tattico'), ('acrobata', 'Acrobata')], max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='InfoAvanzate',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('peso', models.DecimalField(blank=True, decimal_places=1, max_digits=4)),
                ('altezza', models.PositiveSmallIntegerField(blank=True)),
                ('data_nascita', models.DateField(blank=True, default=datetime.date(1900, 1, 1))),
                ('nazionalità', django_countries.fields.CountryField(default='IT', max_length=2)),
                ('numero_telefono', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, region='IT')),
                ('bio', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='PosizioniGioco',
            fields=[
                ('pos_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('preferita', models.CharField(choices=[('POR', 'Portiere'), ('DIF', 'Difensore'), ('CEN', 'Centrocampista'), ('ATT', 'Attaccante'), ('DIF_TER', 'Terzino'), ('CEN_ALA', 'Ala'), ('CEN_TRQ', 'Trequartista'), ('QLS', 'Qualsiasi')], default='QLS', max_length=7)),
                ('alternativa', models.CharField(blank=True, choices=[('POR', 'Portiere'), ('DIF', 'Difensore'), ('CEN', 'Centrocampista'), ('ATT', 'Attaccante'), ('DIF_TER', 'Terzino'), ('CEN_ALA', 'Ala'), ('CEN_TRQ', 'Trequartista'), ('QLS', 'Qualsiasi')], default='QLS', max_length=7)),
                ('alternativa2', models.CharField(blank=True, choices=[('POR', 'Portiere'), ('DIF', 'Difensore'), ('CEN', 'Centrocampista'), ('ATT', 'Attaccante'), ('DIF_TER', 'Terzino'), ('CEN_ALA', 'Ala'), ('CEN_TRQ', 'Trequartista'), ('QLS', 'Qualsiasi')], default='QLS', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='AvatarUtente',
            fields=[
                ('img_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='userInfo.infoavanzate')),
                ('image', models.ImageField(upload_to=userInfo.models.AvatarUtente.uploadTo)),
            ],
        ),
    ]
