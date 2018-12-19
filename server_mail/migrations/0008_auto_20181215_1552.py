# Generated by Django 2.1.3 on 2018-12-15 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_mail', '0007_auto_20181215_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=20, verbose_name='发送规则')),
                ('description', models.CharField(max_length=50, verbose_name='规则描述')),
            ],
            options={
                'verbose_name': '发送规则',
                'verbose_name_plural': '发送规则',
            },
        ),
        migrations.AddField(
            model_name='mailoperation',
            name='send_rules',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='server_mail.SendRule'),
        ),
    ]