# Generated by Django 3.1.4 on 2020-12-20 09:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('display_name', models.CharField(max_length=35, unique=True)),
                ('user_id', models.UUIDField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('country', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_worth', models.FloatField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='api.user')),
            ],
            options={
                'db_table': 'user_score',
            },
        ),
    ]
