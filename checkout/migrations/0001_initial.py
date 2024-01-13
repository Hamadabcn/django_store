# Generated by Django 5.0 on 2024-01-11 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('items', models.JSONField(default=dict)),
                ('customer', models.JSONField(default=dict)),
                ('status', models.IntegerField(choices=[(0, 'Pending Transaction'), (1, 'Completed Transaction')], default=0)),
                ('payment_method', models.IntegerField(choices=[(1, 'Stripe'), (2, 'Paypal')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
