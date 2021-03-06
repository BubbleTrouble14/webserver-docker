# Generated by Django 4.0 on 2021-12-14 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_name', models.CharField(max_length=64)),
                ('confirmed_index', models.BigIntegerField()),
                ('spent_index', models.BigIntegerField()),
                ('spent', models.IntegerField()),
                ('coinbase', models.IntegerField()),
                ('puzzle_hash', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=64)),
                ('coin_parent', models.CharField(max_length=64)),
                ('amount', models.BigIntegerField()),
            ],
            options={
                'db_table': 'coin_record',
            },
        ),
    ]
