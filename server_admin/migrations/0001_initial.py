# Generated by Django 2.1.3 on 2018-12-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.IntegerField(db_column='userId', primary_key=True, serialize=False, verbose_name='用户id')),
                ('useridentity', models.CharField(db_column='userIdentity', max_length=50, verbose_name='用户身份')),
                ('password', models.CharField(blank=True, db_column='passWord', max_length=50, null=True, verbose_name='密码')),
                ('emailaddress', models.CharField(blank=True, db_column='emailAddress', max_length=32, null=True, verbose_name='邮件地址')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'User',
                'managed': False,
            },
        ),
    ]