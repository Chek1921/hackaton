# Generated by Django 4.1.7 on 2023-03-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_site', '0003_report_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='report',
            name='cost',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость услуги'),
        ),
    ]
