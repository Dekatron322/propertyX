# Generated by Django 5.1 on 2024-09-16 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_solicitor_reserveproperty_solicitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitor',
            name='facebook',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='solicitor',
            name='instagram',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='solicitor',
            name='likedin',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='solicitor',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='solicitor',
            name='phone_number',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='solicitor',
            name='position',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='solicitor',
            name='twitter',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
