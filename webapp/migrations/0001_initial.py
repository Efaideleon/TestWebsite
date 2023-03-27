# Generated by Django 4.1.7 on 2023-03-26 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dataMCU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soil_moisture', models.IntegerField()),
                ('soil_temp', models.FloatField()),
            ],
            options={
                'db_table': 'dataMCU',
                'managed': True,
            },
        ),
    ]
