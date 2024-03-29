# Generated by Django 4.2.6 on 2024-01-07 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0003_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='clients.client'),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.transaction'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
