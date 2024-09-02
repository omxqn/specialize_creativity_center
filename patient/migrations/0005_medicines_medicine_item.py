# Generated by Django 3.2.23 on 2024-02-10 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharamacy', '0002_auto_20240108_1343'),
        ('patient', '0004_auto_20231217_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicines',
            name='medicine_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pharamacy.product'),
        ),
    ]
