# Generated by Django 3.2.7 on 2021-11-14 18:58

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20211114_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+27677875278', max_length=128, region=None),
            preserve_default=False,
        ),
    ]
