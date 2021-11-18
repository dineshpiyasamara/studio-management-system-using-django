# Generated by Django 3.2.8 on 2021-11-14 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20211112_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('qty', models.IntegerField()),
                ('product_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.item')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.suppliers')),
            ],
        ),
    ]
