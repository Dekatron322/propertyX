# Generated by Django 5.1 on 2024-09-07 19:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_scheduletour'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('prop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.appuser')),
            ],
        ),
    ]
