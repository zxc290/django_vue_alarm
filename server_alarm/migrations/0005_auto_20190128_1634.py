# Generated by Django 2.1.3 on 2019-01-28 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_alarm', '0004_alarm_receivers_by_games'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameoperation',
            name='alarms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='go_alarms', to='server_alarm.Alarm', verbose_name='操作规则'),
        ),
        migrations.AlterField(
            model_name='gameoperation',
            name='rules',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='go_rules', to='server_alarm.Rule', verbose_name='发送规则'),
        ),
    ]
