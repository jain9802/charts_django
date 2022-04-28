# Generated by Django 4.0.4 on 2022-04-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='supermarket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('customer_type', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('unit_price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('product_line', models.CharField(max_length=50)),
                ('tax', models.FloatField()),
                ('total', models.FloatField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('payment', models.CharField(max_length=50)),
                ('cogs', models.FloatField()),
                ('profit', models.FloatField()),
                ('rating', models.FloatField()),
            ],
        ),
    ]
