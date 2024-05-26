# Generated by Django 5.0.6 on 2024-05-26 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_pay_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='pay',
            name='session_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID сессии'),
        ),
    ]
