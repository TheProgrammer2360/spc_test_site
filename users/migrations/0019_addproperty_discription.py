# Generated by Django 3.2.7 on 2021-12-06 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_addproperty_main_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproperty',
            name='discription',
            field=models.TextField(default='this area is good for students'),
            preserve_default=False,
        ),
    ]