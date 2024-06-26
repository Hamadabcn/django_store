# Generated by Django 5.0.1 on 2024-06-27 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_author_bio_ar_author_bio_en_author_name_ar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='bio_ar',
        ),
        migrations.RemoveField(
            model_name='author',
            name='bio_en',
        ),
        migrations.RemoveField(
            model_name='author',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='author',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='course',
            name='description_ar',
        ),
        migrations.RemoveField(
            model_name='course',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title_ar',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description_ar',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='short_description_ar',
        ),
        migrations.RemoveField(
            model_name='product',
            name='short_description_en',
        ),
    ]
