# Generated by Django 5.0.1 on 2024-06-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_author_bio_ar_author_name_ar_category_name_ar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name_ar',
            field=models.CharField(default='اسم افتراضي', max_length=255, verbose_name='اسم'),
        ),
    ]
