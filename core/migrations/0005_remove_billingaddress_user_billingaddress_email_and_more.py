# Generated by Django 5.0.6 on 2024-06-04 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='user',
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='full_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='street_address',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
