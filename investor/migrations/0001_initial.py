# Generated by Django 4.2.6 on 2024-01-07 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('is_credit', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=191, null=True)),
                ('type', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('fullname', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('currency', models.CharField(blank=True, max_length=20, null=True)),
                ('chat_id', models.CharField(blank=True, max_length=100, null=True)),
                ('investor_status', models.CharField(choices=[('active', 'active'), ('deactive', 'deactive')], default='active', max_length=31)),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
    ]