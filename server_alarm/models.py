# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import hashlib
from django.db import models, connections
from django.conf import settings
from .model_managers import UserWithEmailManager, OnlineAppManager, ServerManagementManager, ServerMailManager
from .dbtools import dict_fetchall

class User(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True, verbose_name='用户id')  # Field name made lowercase.
    useridentity = models.CharField(db_column='userIdentity', max_length=50, verbose_name='用户身份')  # Field name made lowercase.
    password = models.CharField(db_column='passWord', max_length=50, blank=True, null=True, verbose_name='密码')  # Field name made lowercase.
    emailaddress = models.CharField(db_column='emailAddress', max_length=32, blank=True, null=True, verbose_name='邮箱地址')  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=11, blank=True, null=True, verbose_name='电话号码')  # Field name made lowercase.
    ipaddress = models.CharField(db_column='ipAddress', max_length=16, blank=True, null=True, verbose_name='ip地址')  # Field name made lowercase.
    mac = models.CharField(max_length=32, blank=True, null=True, verbose_name='mac地址')
    username = models.CharField(db_column='userName', max_length=50, blank=True, null=True, verbose_name='用户名')  # Field name made lowercase.
    admin = models.IntegerField(blank=True, null=True, verbose_name='管理员')
    failcount = models.IntegerField(db_column='failCount', blank=True, null=True, verbose_name='登录失败次数')  # Field name made lowercase.
    lastlogintime = models.IntegerField(db_column='lastLoginTime', blank=True, null=True, verbose_name='最后登录时间')  # Field name made lowercase.
    token = models.CharField(max_length=32, blank=True, null=True, verbose_name='token令牌')

    def check_password(self, password):
        return hashlib.md5(password.encode()).hexdigest().upper() == self.password

    objects = UserWithEmailManager()

    def get_user_permission(self):
        sql = "SELECT * FROM dbo.NAuth({user_id}, 3) WHERE PID > 0 and FID IN {fid_permission}".format(user_id=self.userid, fid_permission=settings.FID_PERMISSION)
        try:
            admin_cursor = connections['default'].cursor()
            admin_cursor.execute(sql)
            result = dict_fetchall(admin_cursor)
            return result
        except:
            return False

    def __str__(self):
        return self.useridentity

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'User'


class ServerTable(models.Model):
    idx = models.IntegerField(primary_key=True, verbose_name='服务器id')
    zonename = models.CharField(db_column='ZoneName', max_length=1024, blank=True, null=True, verbose_name='区名')  # Field name made lowercase.
    zoneid = models.IntegerField(db_column='ZoneId', blank=True, null=True, verbose_name='区id')  # Field name made lowercase.
    ptid = models.IntegerField(db_column='Ptid', blank=True, null=True, verbose_name='平台id')  # Field name made lowercase.
    ptname = models.CharField(db_column='PtName', max_length=20, blank=True, null=True, verbose_name='平台名')  # Field name made lowercase.
    svrid = models.CharField(db_column='SvrId', max_length=50, blank=True, null=True, verbose_name='服务器id')  # Field name made lowercase.
    svrtype = models.CharField(db_column='SvrType', max_length=20, blank=True, null=True, verbose_name='服务器类型')  # Field name made lowercase.
    gametypeno = models.IntegerField(db_column='GameTypeno', verbose_name='游戏号')  # Field name made lowercase.
    gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True, verbose_name='游戏类型')  # Field name made lowercase.
    ipadd = models.CharField(db_column='IpAdd', max_length=30, blank=True, null=True, verbose_name='ip地址')  # Field name made lowercase.
    dev_id = models.IntegerField(db_column='Dev_id', blank=True, null=True, verbose_name='设备id')  # Field name made lowercase.
    domainname = models.CharField(db_column='DomainName', max_length=50, blank=True, null=True, verbose_name='域名')  # Field name made lowercase.
    h_s_info = models.CharField(db_column='H&S_info', max_length=50, blank=True, null=True, verbose_name='hs信息')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    servermanagerport = models.IntegerField(db_column='ServermanagerPort', blank=True, null=True, verbose_name='servermanager端口')  # Field name made lowercase.
    lock = models.IntegerField(db_column='Lock', blank=True, null=True, verbose_name='锁')  # Field name made lowercase.
    prostat = models.IntegerField(blank=True, null=True, verbose_name='pro状态')
    logzoneid = models.IntegerField(db_column='LogZoneId', blank=True, null=True, verbose_name='区日志id')  # Field name made lowercase.
    logsvrip_in = models.CharField(db_column='LogSvrIp_in', max_length=30, blank=True, null=True, verbose_name='内网日志服务器ip')  # Field name made lowercase.
    logdb_in = models.CharField(db_column='LogDB_in', max_length=50, blank=True, null=True, verbose_name='内网日志数据库')  # Field name made lowercase.
    loguid_in = models.CharField(db_column='LogUid_in', max_length=50, blank=True, null=True, verbose_name='内网日志数据库用户')  # Field name made lowercase.
    logpwd_in = models.CharField(db_column='LogPwd_in', max_length=50, blank=True, null=True, verbose_name='内网日志数据库密码')  # Field name made lowercase.
    logsvrip_out = models.CharField(db_column='LogSvrIp_out', max_length=30, blank=True, null=True, verbose_name='外网日志服务器ip')  # Field name made lowercase.
    logdb_out = models.CharField(db_column='LogDB_out', max_length=50, blank=True, null=True, verbose_name='外网日志数据库')  # Field name made lowercase.
    loguid_out = models.CharField(db_column='LogUid_out', max_length=50, blank=True, null=True, verbose_name='外网日志数据库用户')  # Field name made lowercase.
    logpwd_out = models.CharField(db_column='LogPwd_out', max_length=50, blank=True, null=True, verbose_name='外网日志数据库密码')  # Field name made lowercase.
    hequ = models.CharField(db_column='HeQu', max_length=50, blank=True, null=True, verbose_name='合区')  # Field name made lowercase.
    kaiqu_time = models.CharField(max_length=50, verbose_name='开区时间')
    hequid = models.CharField(max_length=50, blank=True, null=True, verbose_name='合区id')
    hequidx = models.IntegerField(blank=True, null=True, verbose_name='合区idx')
    serverpath = models.CharField(db_column='ServerPath', max_length=50, blank=True, null=True, verbose_name='服务器路径')  # Field name made lowercase.
    loginport = models.CharField(db_column='LoginPort', max_length=50, blank=True, null=True, verbose_name='登录端口')  # Field name made lowercase.
    rmbport = models.IntegerField(db_column='RmbPort', blank=True, null=True, verbose_name='人民币端口')  # Field name made lowercase.
    db_svrcfg = models.CharField(max_length=50, blank=True, null=True, verbose_name='svrcfg数据库')
    db_player = models.CharField(max_length=50, blank=True, null=True, verbose_name='player数据库')
    db_login = models.CharField(max_length=50, blank=True, null=True, verbose_name='login数据库')
    db_super = models.CharField(max_length=50, blank=True, null=True, verbose_name='super数据库')
    db_rmb = models.CharField(max_length=50, blank=True, null=True, verbose_name='rmb数据库')
    db_param = models.CharField(max_length=50, blank=True, null=True, verbose_name='param数据库')
    trigger_flag = models.CharField(max_length=50, blank=True, null=True, verbose_name='触发器')

    objects = ServerManagementManager()

    def __str__(self):
        return self.ipadd

    class Meta:
        verbose_name = '服务器列表'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'Server_table'


class AppList(models.Model):
    gid = models.IntegerField(db_column='GID', primary_key=True, verbose_name='游戏id')  # Field name made lowercase.
    gname = models.CharField(db_column='GName', max_length=50, blank=True, null=True, verbose_name='游戏名称')  # Field name made lowercase.
    gtype = models.IntegerField(db_column='GType', blank=True, null=True, verbose_name='游戏类型')  # Field name made lowercase.
    createdate = models.DateField(db_column='CreateDate', blank=True, null=True, verbose_name='创建时间')  # Field name made lowercase.
    testdate = models.DateField(db_column='TestDate', blank=True, null=True, verbose_name='测试时间')  # Field name made lowercase.
    onlinedate = models.DateField(db_column='OnlineDate', blank=True, null=True, verbose_name='上线时间')  # Field name made lowercase.
    offlinedate = models.DateField(db_column='OfflineDate', blank=True, null=True, verbose_name='下线时间')  # Field name made lowercase.
    supervisor = models.CharField(db_column='Supervisor', max_length=50, blank=True, null=True, verbose_name='监管人员')  # Field name made lowercase.

    objects = OnlineAppManager()

    def __str__(self):
        return self.gname

    class Meta:
        verbose_name = '游戏列表'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'App_list'


class Rule(models.Model):
    send_rule = models.CharField(max_length=20, verbose_name='发送规则')
    description = models.CharField(max_length=50, verbose_name='规则描述')

    objects = ServerMailManager()

    def __str__(self):
        return self.send_rule

    class Meta:
        verbose_name = '发送规则'
        verbose_name_plural = verbose_name


class Alarm(models.Model):
    type = models.CharField(max_length=20, verbose_name='报警类型', unique=True)
    description = models.CharField(max_length=20, verbose_name='报警描述')
    receivers = models.CharField(max_length=1000, blank=True, null=True, verbose_name='收件人列表')
    receivers_by_games = models.BooleanField(verbose_name='是否按游戏区分', default=False)
    json_args = models.CharField(max_length=50, verbose_name='前端参数')
    template_kwargs = models.CharField(max_length=50, verbose_name='模板参数')
    # send_rules = models.ForeignKey(SendRule, on_delete=models.SET_NULL, null=True, verbose_name='发送规则')
    rules = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='alarms', verbose_name='发送规则')

    objects = ServerMailManager()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = '邮件规则'
        verbose_name_plural = verbose_name


class GameOperation(models.Model):
    game = models.CharField(max_length=20, verbose_name='游戏', null=True, blank=True)
    receivers = models.CharField(max_length=1000, verbose_name='收件人', blank=True, null=True, default='')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    alarms = models.ForeignKey(Alarm, on_delete=models.CASCADE, related_name='go_alarms', verbose_name='操作规则')
    rules = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='go_rules', verbose_name='发送规则', null=True)

    objects = ServerMailManager()

    def __str__(self):
        return self.game + '_' + self.alarms.description

    def get_game_info(self, data):
        self.ip = data.get('ip', '')
        self.game = data.get('game', '')
        self.platform = data.get('platform', '')
        self.zone = data.get('zone', '')

    class Meta:
        ordering = ['-created_date']
        verbose_name = '邮件操作'
        verbose_name_plural = verbose_name


class MailInfo(models.Model):
    ip_address = models.CharField(max_length=15, verbose_name='IP地址', null=True, blank=True)
    game = models.CharField(max_length=100, verbose_name='游戏', null=True, blank=True)
    platform = models.CharField(max_length=100, verbose_name='平台', null=True, blank=True)
    zone = models.CharField(max_length=100, verbose_name='区服', null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.CharField(max_length=100, verbose_name='内容')
    sent = models.BooleanField(default=False, verbose_name='已发送')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    alarms = models.ManyToManyField(Alarm, verbose_name='邮件类型')

    objects = ServerMailManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']
        verbose_name = '邮件信息'
        verbose_name_plural = verbose_name