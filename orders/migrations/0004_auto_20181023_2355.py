# Generated by Django 2.0.3 on 2018-10-24 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20181023_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incart',
            old_name='ammount',
            new_name='amount',
        ),
    ]