# Generated by Django 2.0.3 on 2018-10-21 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
                ('picture', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=64)),
                ('last', models.CharField(max_length=64)),
                ('money', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='orders.User'),
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='orders.Product'),
        ),
    ]
