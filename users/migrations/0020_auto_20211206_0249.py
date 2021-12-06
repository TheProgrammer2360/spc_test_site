# Generated by Django 3.2.7 on 2021-12-06 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_addproperty_discription'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproperty',
            name='hot_water',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addproperty',
            name='price',
            field=models.FloatField(default=23.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addproperty',
            name='security',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
