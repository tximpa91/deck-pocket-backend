# Generated by Django 3.0.7 on 2020-09-22 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deck_pocket', '0022_card_printed_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
