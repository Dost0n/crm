# Generated by Django 4.2.6 on 2024-01-07 21:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('fullname', models.CharField(max_length=200)),
                ('passport', models.CharField(max_length=20)),
                ('pinfl', models.CharField(max_length=14)),
                ('phone_number', models.CharField(max_length=20)),
                ('phone_number2', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('active', 'active'), ('deactive', 'deactive')], default='deactive', max_length=31)),
                ('contract', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('product', models.CharField(blank=True, max_length=191, null=True)),
                ('product_code', models.CharField(blank=True, max_length=20, null=True)),
                ('contract_date', models.DateField(blank=True, null=True)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('product_price', models.FloatField(blank=True, null=True)),
                ('loan_amount', models.FloatField(blank=True, null=True)),
                ('consumption', models.FloatField(blank=True, null=True)),
                ('initial_payment', models.FloatField(blank=True, null=True)),
                ('percentage', models.FloatField(blank=True, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('total_debit', models.FloatField(blank=True, null=True)),
                ('current_debit', models.FloatField(blank=True, null=True)),
                ('income_amount', models.FloatField(blank=True, null=True)),
                ('real_income', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Graphic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('paid_amount', models.FloatField(blank=True, null=True)),
                ('remaining_amount', models.FloatField(blank=True, null=True)),
                ('month', models.DateField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('is_calc', models.IntegerField(blank=True, null=True)),
                ('delayed', models.IntegerField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='graphics', to='clients.client')),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='clients/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='clients.client')),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=4)),
                ('expiration_time', models.DateTimeField(null=True)),
                ('is_isconfirmed', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verify_codes', to='clients.client')),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
    ]