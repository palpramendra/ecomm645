# Generated by Django 4.1.3 on 2022-11-29 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_productreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True)),
                ('username', models.CharField(max_length=300)),
                ('slug', models.CharField(max_length=500)),
                ('quantity', models.ImageField(upload_to='')),
                ('total', models.IntegerField()),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
            ],
        ),
    ]
