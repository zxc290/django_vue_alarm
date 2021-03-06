# Generated by Django 2.1.3 on 2019-01-28 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppList',
            fields=[
                ('gid', models.IntegerField(db_column='GID', primary_key=True, serialize=False, verbose_name='游戏id')),
                ('gname', models.CharField(blank=True, db_column='GName', max_length=50, null=True, verbose_name='游戏名称')),
                ('gtype', models.IntegerField(blank=True, db_column='GType', null=True, verbose_name='游戏类型')),
                ('createdate', models.DateField(blank=True, db_column='CreateDate', null=True, verbose_name='创建时间')),
                ('testdate', models.DateField(blank=True, db_column='TestDate', null=True, verbose_name='测试时间')),
                ('onlinedate', models.DateField(blank=True, db_column='OnlineDate', null=True, verbose_name='上线时间')),
                ('offlinedate', models.DateField(blank=True, db_column='OfflineDate', null=True, verbose_name='下线时间')),
                ('supervisor', models.CharField(blank=True, db_column='Supervisor', max_length=50, null=True, verbose_name='监管人员')),
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
                ('zonename', models.CharField(blank=True, db_column='ZoneName', max_length=1024, null=True, verbose_name='区名')),
                ('zoneid', models.IntegerField(blank=True, db_column='ZoneId', null=True, verbose_name='区id')),
                ('ptid', models.IntegerField(blank=True, db_column='Ptid', null=True, verbose_name='平台id')),
                ('ptname', models.CharField(blank=True, db_column='PtName', max_length=20, null=True, verbose_name='平台名')),
                ('svrid', models.CharField(blank=True, db_column='SvrId', max_length=50, null=True, verbose_name='服务器id')),
                ('svrtype', models.CharField(blank=True, db_column='SvrType', max_length=20, null=True, verbose_name='服务器类型')),
                ('gametypeno', models.IntegerField(db_column='GameTypeno', verbose_name='游戏号')),
                ('gametype', models.CharField(blank=True, db_column='GameType', max_length=20, null=True, verbose_name='游戏类型')),
                ('ipadd', models.CharField(blank=True, db_column='IpAdd', max_length=30, null=True, verbose_name='ip地址')),
                ('dev_id', models.IntegerField(blank=True, db_column='Dev_id', null=True, verbose_name='设备id')),
                ('domainname', models.CharField(blank=True, db_column='DomainName', max_length=50, null=True, verbose_name='域名')),
                ('h_s_info', models.CharField(blank=True, db_column='H&S_info', max_length=50, null=True, verbose_name='hs信息')),
                ('servermanagerport', models.IntegerField(blank=True, db_column='ServermanagerPort', null=True, verbose_name='servermanager端口')),
                ('lock', models.IntegerField(blank=True, db_column='Lock', null=True, verbose_name='锁')),
                ('prostat', models.IntegerField(blank=True, null=True, verbose_name='pro状态')),
                ('logzoneid', models.IntegerField(blank=True, db_column='LogZoneId', null=True, verbose_name='区日志id')),
                ('logsvrip_in', models.CharField(blank=True, db_column='LogSvrIp_in', max_length=30, null=True, verbose_name='内网日志服务器ip')),
                ('logdb_in', models.CharField(blank=True, db_column='LogDB_in', max_length=50, null=True, verbose_name='内网日志数据库')),
                ('loguid_in', models.CharField(blank=True, db_column='LogUid_in', max_length=50, null=True, verbose_name='内网日志数据库用户')),
                ('logpwd_in', models.CharField(blank=True, db_column='LogPwd_in', max_length=50, null=True, verbose_name='内网日志数据库密码')),
                ('logsvrip_out', models.CharField(blank=True, db_column='LogSvrIp_out', max_length=30, null=True, verbose_name='外网日志服务器ip')),
                ('logdb_out', models.CharField(blank=True, db_column='LogDB_out', max_length=50, null=True, verbose_name='外网日志数据库')),
                ('loguid_out', models.CharField(blank=True, db_column='LogUid_out', max_length=50, null=True, verbose_name='外网日志数据库用户')),
                ('logpwd_out', models.CharField(blank=True, db_column='LogPwd_out', max_length=50, null=True, verbose_name='外网日志数据库密码')),
                ('hequ', models.CharField(blank=True, db_column='HeQu', max_length=50, null=True, verbose_name='合区')),
                ('kaiqu_time', models.CharField(max_length=50, verbose_name='开区时间')),
                ('hequid', models.CharField(blank=True, max_length=50, null=True, verbose_name='合区id')),
                ('hequidx', models.IntegerField(blank=True, null=True, verbose_name='合区idx')),
                ('serverpath', models.CharField(blank=True, db_column='ServerPath', max_length=50, null=True, verbose_name='服务器路径')),
                ('loginport', models.CharField(blank=True, db_column='LoginPort', max_length=50, null=True, verbose_name='登录端口')),
                ('rmbport', models.IntegerField(blank=True, db_column='RmbPort', null=True, verbose_name='人民币端口')),
                ('db_svrcfg', models.CharField(blank=True, max_length=50, null=True, verbose_name='svrcfg数据库')),
                ('db_player', models.CharField(blank=True, max_length=50, null=True, verbose_name='player数据库')),
                ('db_login', models.CharField(blank=True, max_length=50, null=True, verbose_name='login数据库')),
                ('db_super', models.CharField(blank=True, max_length=50, null=True, verbose_name='super数据库')),
                ('db_rmb', models.CharField(blank=True, max_length=50, null=True, verbose_name='rmb数据库')),
                ('db_param', models.CharField(blank=True, max_length=50, null=True, verbose_name='param数据库')),
                ('trigger_flag', models.CharField(blank=True, max_length=50, null=True, verbose_name='触发器')),
            ],
            options={
                'verbose_name': '服务器列表',
                'verbose_name_plural': '服务器列表',
                'db_table': 'Server_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.IntegerField(db_column='userId', primary_key=True, serialize=False, verbose_name='用户id')),
                ('useridentity', models.CharField(db_column='userIdentity', max_length=50, verbose_name='用户身份')),
                ('password', models.CharField(blank=True, db_column='passWord', max_length=50, null=True, verbose_name='密码')),
                ('emailaddress', models.CharField(blank=True, db_column='emailAddress', max_length=32, null=True, verbose_name='邮箱地址')),
                ('phonenumber', models.CharField(blank=True, db_column='phoneNumber', max_length=11, null=True, verbose_name='电话号码')),
                ('ipaddress', models.CharField(blank=True, db_column='ipAddress', max_length=16, null=True, verbose_name='ip地址')),
                ('mac', models.CharField(blank=True, max_length=32, null=True, verbose_name='mac地址')),
                ('username', models.CharField(blank=True, db_column='userName', max_length=50, null=True, verbose_name='用户名')),
                ('admin', models.IntegerField(blank=True, null=True, verbose_name='管理员')),
                ('failcount', models.IntegerField(blank=True, db_column='failCount', null=True, verbose_name='登录失败次数')),
                ('lastlogintime', models.IntegerField(blank=True, db_column='lastLoginTime', null=True, verbose_name='最后登录时间')),
                ('token', models.CharField(blank=True, max_length=32, null=True, verbose_name='token令牌')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'User',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, unique=True, verbose_name='报警类型')),
                ('description', models.CharField(max_length=20, verbose_name='报警描述')),
                ('receivers', models.CharField(max_length=1000, verbose_name='收件人列表')),
                ('json_args', models.CharField(default='', max_length=50, verbose_name='前端参数')),
                ('template_kwargs', models.CharField(default='', max_length=50, verbose_name='模板参数')),
            ],
            options={
                'verbose_name': '邮件规则',
                'verbose_name_plural': '邮件规则',
            },
        ),
        migrations.CreateModel(
            name='GameOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.CharField(blank=True, max_length=20, null=True, verbose_name='游戏')),
                ('receivers', models.CharField(max_length=1000, verbose_name='收件人')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('alarms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mail_operations_alarms', to='server_alarm.Alarm', verbose_name='操作规则')),
            ],
            options={
                'verbose_name': '邮件操作',
                'verbose_name_plural': '邮件操作',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='MailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, max_length=15, null=True, verbose_name='IP地址')),
                ('game', models.CharField(blank=True, max_length=20, null=True, verbose_name='游戏')),
                ('platform', models.CharField(blank=True, max_length=20, null=True, verbose_name='平台')),
                ('zone', models.CharField(blank=True, max_length=20, null=True, verbose_name='区服')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('content', models.CharField(max_length=50, verbose_name='内容')),
                ('sent', models.BooleanField(default=False, verbose_name='已发送')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('alarms', models.ManyToManyField(to='server_alarm.Alarm', verbose_name='邮件类型')),
            ],
            options={
                'verbose_name': '邮件信息',
                'verbose_name_plural': '邮件信息',
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_rule', models.CharField(max_length=20, verbose_name='发送规则')),
                ('description', models.CharField(max_length=50, verbose_name='规则描述')),
            ],
            options={
                'verbose_name': '发送规则',
                'verbose_name_plural': '发送规则',
            },
        ),
        migrations.AddField(
            model_name='gameoperation',
            name='rules',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mail_operations_rules', to='server_alarm.Rule', verbose_name='发送规则'),
        ),
        migrations.AddField(
            model_name='alarm',
            name='rules',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to='server_alarm.Rule', verbose_name='发送规则'),
        ),
    ]
