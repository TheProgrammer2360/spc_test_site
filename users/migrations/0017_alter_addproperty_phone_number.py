# Generated by Django 3.2.7 on 2021-12-03 03:49

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_addproperty_university_catered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproperty',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]