# Generated by Django 3.2.7 on 2021-12-02 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20211201_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproperty',
            name='university_catered',
            field=models.CharField(choices=[('UJ1', 'UJ(APK)'), ('UJ2', 'UJ(APB)'), ('UJ3', 'UJ(DFC)'), ('UJ4', 'UJ(  SWC)'), ('NWU1', 'NWU-Mafikeng campus'), ('NWU2', 'NWU-Vaal campus'), ('NWU3', 'NWU-Potchefstroom campus'), ('TUT', 'TUT'), ('WITS', 'WITS'), ('UP', 'WITS'), ('CUT', 'CUT'), ('VUT', 'VUT'), ('UWC', 'UWC'), ('UFS', 'UFS')], max_length=4),
        ),
    ]
