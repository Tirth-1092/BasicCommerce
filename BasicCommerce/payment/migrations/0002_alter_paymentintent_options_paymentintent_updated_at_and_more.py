# Generated by Django 5.1.6 on 2025-03-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentintent',
            options={'ordering': ['-created_at'], 'verbose_name': 'Payment Intent', 'verbose_name_plural': 'Payment Intents'},
        ),
        migrations.AddField(
            model_name='paymentintent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='stripe_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paymentintent',
            name='status',
            field=models.CharField(choices=[('requires_payment_method', 'Requires Payment Method'), ('requires_confirmation', 'Requires Confirmation'), ('succeeded', 'Succeeded'), ('failed', 'Failed')], max_length=100),
        ),
    ]
