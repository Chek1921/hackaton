# Generated by Django 4.1.7 on 2023-03-25 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_site', '0002_remove_customuser_want_work_userrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стоимость услуги'),
        ),
    ]
