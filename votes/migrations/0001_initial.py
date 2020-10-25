# Generated by Django 3.1 on 2020-10-17 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('voters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.CharField(max_length=60)),
                ('position', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votecarts', to='voters.voter')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='voters.voter')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
