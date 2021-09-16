# Generated by Django 3.2.7 on 2021-09-15 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_auto_20210915_1032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounttier',
            old_name='account_tier',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='accounttier',
            name='user',
        ),
        migrations.CreateModel(
            name='UserTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_tier', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.accounttier')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TierSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_size', models.PositiveSmallIntegerField()),
                ('tier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.accounttier')),
            ],
        ),
    ]
