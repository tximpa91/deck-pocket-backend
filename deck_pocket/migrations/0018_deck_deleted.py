# Generated by Django 3.0.7 on 2020-07-26 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deck_pocket', '0017_mkmlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]