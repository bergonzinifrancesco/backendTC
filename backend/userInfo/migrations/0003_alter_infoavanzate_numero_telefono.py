# Generated by Django 4.2.3 on 2023-07-25 20:13

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('userInfo', '0002_alter_caratteristichegioco_car_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoavanzate',
            name='numero_telefono',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, region='IT'),
        ),
    ]