# Generated by Django 2.2.4 on 2019-09-02 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('parent', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('nutriscore', models.CharField(max_length=1)),
                ('image_url', models.URLField()),
                ('product_url', models.URLField(default='')),
                ('purchase_places', models.CharField(max_length=100, null=True)),
                ('energy_100g', models.FloatField(null=True)),
                ('fat_100g', models.FloatField(null=True)),
                ('saturated_fats_100g', models.FloatField(null=True)),
                ('carbohydrates_100g', models.FloatField(null=True)),
                ('sugars_100g', models.FloatField(null=True)),
                ('fibers_100g', models.FloatField(null=True)),
                ('proteins_100g', models.FloatField(null=True)),
                ('salt_100g', models.FloatField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
                ('favorite', models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
