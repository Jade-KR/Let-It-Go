# Generated by Django 3.0.6 on 2020-06-12 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200612_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subset',
            name='legoset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_set', to='api.LegoSet'),
        ),
    ]
