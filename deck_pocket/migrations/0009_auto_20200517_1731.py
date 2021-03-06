# Generated by Django 3.0.6 on 2020-05-17 15:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('deck_pocket', '0008_auto_20200510_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='cards',
        ),
        migrations.CreateModel(
            name='CardForDeck',
            fields=[
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(blank=True, db_column='updated', null=True)),
                ('card_for_deck_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('have_it', models.BooleanField(default=False)),
                ('card', models.ForeignKey(blank=True, db_column='card_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_for_deck', to='deck_pocket.Card')),
                ('deck', models.ForeignKey(blank=True, db_column='deck_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deck_for_card', to='deck_pocket.Deck')),
            ],
            options={
                'db_table': 'CardForDeck',
            },
        ),
    ]
