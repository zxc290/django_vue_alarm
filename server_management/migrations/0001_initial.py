# Generated by Django 2.1.3 on 2018-12-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppList',
            fields=[
                ('gid', models.IntegerField(db_column='GID', primary_key=True, serialize=False, verbose_name='游戏id')),
                ('gname', models.CharField(blank=True, db_column='GName', max_length=50, null=True, verbose_name='游戏名')),
                ('onlinedate', models.DateField(blank=True, db_column='OnlineDate', null=True, verbose_name='开服时间')),
                ('offlinedate', models.DateField(blank=True, db_column='OfflineDate', null=True, verbose_name='关服时间')),
            ],
            options={
                'verbose_name': '游戏列表',
                'verbose_name_plural': '游戏列表',
                'db_table': 'App_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServerTable',
            fields=[
                ('idx', models.IntegerField(primary_key=True, serialize=False, verbose_name='服务器id')),
                ('gametype', models.CharField(blank=True, db_column='GameType', max_length=20, null=True, verbose_name='游戏类型')),
                ('ipadd', models.CharField(blank=True, db_column='IpAdd', max_length=30, null=True, verbose_name='ip地址')),
                ('ptname', models.CharField(blank=True, db_column='PtName', max_length=20, null=True, verbose_name='平台')),
                ('zonename', models.CharField(blank=True, db_column='ZoneName', max_length=1024, null=True, verbose_name='区服')),
            ],
            options={
                'verbose_name': '服务器列表',
                'verbose_name_plural': '服务器列表',
                'db_table': 'Server_table',
                'managed': False,
            },
        ),
    ]