# Generated by Django 3.1.6 on 2022-07-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0003_auto_20220705_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discounted_price',
        ),
        migrations.AddField(
            model_name='productseller',
            name='discounted_price',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]
