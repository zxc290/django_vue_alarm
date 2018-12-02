# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class OnlineAppManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(onlinedate=None).filter(offlinedate=None)


class AppList(models.Model):
    gid = models.IntegerField(db_column='GID', primary_key=True, verbose_name='游戏id')
    gname = models.CharField(db_column='GName', max_length=50, blank=True, null=True, verbose_name='游戏名')
    onlinedate = models.DateField(db_column='OnlineDate', blank=True, null=True, verbose_name='开服时间')
    offlinedate = models.DateField(db_column='OfflineDate', blank=True, null=True, verbose_name='关服时间')
    # gtype = models.IntegerField(db_column='GType', blank=True, null=True)
    # createdate = models.DateField(db_column='CreateDate', blank=True, null=True)
    # testdate = models.DateField(db_column='TestDate', blank=True, null=True)

    # supervisor = models.CharField(db_column='Supervisor', max_length=50, blank=True, null=True)

    objects = OnlineAppManager()

    def __str__(self):
        return self.gname

    class Meta:
        verbose_name = '游戏列表'
        verbose_name_plural = verbose_name
        app_label = 'server_management'
        managed = False
        db_table = 'App_list'


class ServerTable(models.Model):
    idx = models.IntegerField(primary_key=True, verbose_name='服务器id')
    gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True, verbose_name='游戏类型')
    ipadd = models.CharField(db_column='IpAdd', max_length=30, blank=True, null=True, verbose_name='ip地址')
    # zonename = models.CharField(db_column='ZoneName', max_length=1024, blank=True, null=True)
    # zoneid = models.IntegerField(db_column='ZoneId', blank=True, null=True)
    # ptid = models.IntegerField(db_column='Ptid', blank=True, null=True)
    # ptname = models.CharField(db_column='PtName', max_length=20, blank=True, null=True)
    # svrid = models.CharField(db_column='SvrId', max_length=50, blank=True, null=True)
    # svrtype = models.CharField(db_column='SvrType', max_length=20, blank=True, null=True)
    # gametypeno = models.IntegerField(db_column='GameTypeno')
    # dev_id = models.IntegerField(db_column='Dev_id', blank=True, null=True)
    # domainname = models.CharField(db_column='DomainName', max_length=50, blank=True, null=True)
    # h_s_info = models.CharField(db_column='H&S_info', max_length=50, blank=True, null=True)
    # servermanagerport = models.IntegerField(db_column='ServermanagerPort', blank=True, null=True)
    # lock = models.IntegerField(db_column='Lock', blank=True, null=True)
    # prostat = models.IntegerField(blank=True, null=True)
    # logzoneid = models.IntegerField(db_column='LogZoneId', blank=True, null=True)
    # logsvrip_in = models.CharField(db_column='LogSvrIp_in', max_length=30, blank=True, null=True)
    # logdb_in = models.CharField(db_column='LogDB_in', max_length=50, blank=True, null=True)
    # loguid_in = models.CharField(db_column='LogUid_in', max_length=50, blank=True, null=True)
    # logpwd_in = models.CharField(db_column='LogPwd_in', max_length=50, blank=True, null=True)
    # logsvrip_out = models.CharField(db_column='LogSvrIp_out', max_length=30, blank=True, null=True)
    # logdb_out = models.CharField(db_column='LogDB_out', max_length=50, blank=True, null=True)
    # loguid_out = models.CharField(db_column='LogUid_out', max_length=50, blank=True, null=True)
    # logpwd_out = models.CharField(db_column='LogPwd_out', max_length=50, blank=True, null=True)
    # hequ = models.CharField(db_column='HeQu', max_length=50, blank=True, null=True)
    # kaiqu_time = models.CharField(max_length=50)
    # hequid = models.CharField(max_length=50, blank=True, null=True)
    # hequidx = models.IntegerField(blank=True, null=True)
    # serverpath = models.CharField(db_column='ServerPath', max_length=50, blank=True, null=True)
    # loginport = models.CharField(db_column='LoginPort', max_length=50, blank=True, null=True)
    # rmbport = models.IntegerField(db_column='RmbPort', blank=True, null=True)
    # db_svrcfg = models.CharField(max_length=50, blank=True, null=True)
    # db_player = models.CharField(max_length=50, blank=True, null=True)
    # db_login = models.CharField(max_length=50, blank=True, null=True)
    # db_super = models.CharField(max_length=50, blank=True, null=True)
    # db_rmb = models.CharField(max_length=50, blank=True, null=True)
    # db_param = models.CharField(max_length=50, blank=True, null=True)
    # trigger_flag = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.ipadd

    class Meta:
        verbose_name = '服务器列表'
        verbose_name_plural = verbose_name
        app_label = 'server_management'
        managed = False
        db_table = 'Server_table'


# class AppServerList(models.Model):
#     sid = models.IntegerField(db_column='SID', blank=True, null=True)
#     sname = models.CharField(db_column='SName', max_length=512, blank=True, null=True)
#     pid = models.IntegerField(db_column='PID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     apid = models.IntegerField(db_column='APID', blank=True, null=True)
#     display = models.IntegerField(db_column='Display', blank=True, null=True)
#     devid = models.IntegerField(db_column='DevID', blank=True, null=True)
#     dn = models.CharField(db_column='DN', max_length=50, blank=True, null=True)
#     vid = models.IntegerField(db_column='VID', blank=True, null=True)
#     type = models.IntegerField(db_column='Type', blank=True, null=True)
#     status = models.IntegerField(db_column='Status', blank=True, null=True)
#     prostatus = models.IntegerField(db_column='ProStatus', blank=True, null=True)
#     opendate = models.DateField(db_column='OpenDate')
#     mergedate = models.DateField(db_column='MergeDate')
#     mergeid = models.IntegerField(db_column='MergeID')
#     mergeidx = models.IntegerField(db_column='MergeIdx')
#     serverid = models.IntegerField(db_column='ServerID', blank=True, null=True)
#     gslist = models.CharField(db_column='GSList', max_length=50, blank=True, null=True)
#     dbsvr_in = models.CharField(db_column='DBSvr_in', max_length=50, blank=True, null=True)
#     dbname_in = models.CharField(db_column='DBName_in', max_length=50, blank=True, null=True)
#     dbqueryid_in = models.IntegerField(db_column='DBQueryId_in', blank=True, null=True)
#     dbsvr_out = models.CharField(db_column='DBSvr_out', max_length=50, blank=True, null=True)
#     dbname_out = models.CharField(db_column='DBName_out', max_length=50, blank=True, null=True)
#     dbqueryid_out = models.IntegerField(db_column='DBQueryId_out', blank=True, null=True)
#     serverpath = models.CharField(db_column='ServerPath', max_length=50, blank=True, null=True)
#     smport = models.IntegerField(db_column='SMPort')
#     loginport = models.CharField(db_column='LoginPort', max_length=50, blank=True, null=True)
#     rmbport = models.IntegerField(db_column='RmbPort', blank=True, null=True)
#     db_svrcfg = models.CharField(max_length=50, blank=True, null=True)
#     db_player = models.CharField(max_length=50, blank=True, null=True)
#     db_login = models.CharField(max_length=50, blank=True, null=True)
#     db_super = models.CharField(max_length=50, blank=True, null=True)
#     db_rmb = models.CharField(max_length=50, blank=True, null=True)
#     db_param = models.CharField(max_length=50, blank=True, null=True)
#     trigger_flag = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'APP_Server_list'
#         unique_together = (('sid', 'pid', 'gid'),)
#
#
# class AppChannelList(models.Model):
#     cid = models.AutoField(db_column='CID', primary_key=True)
#     cname = models.CharField(db_column='CName', max_length=50, blank=True, null=True)
#     cinfo = models.CharField(db_column='CInfo', max_length=512, blank=True, null=True)
#     pid = models.IntegerField(db_column='PID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'App_Channel_list'
#         unique_together = (('cname', 'pid', 'gid'),)
#
#
# class AppPlatformCfg(models.Model):
#     idx = models.AutoField()
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     pid = models.IntegerField(db_column='PID', blank=True, null=True)
#     pname = models.CharField(db_column='PName', max_length=50, blank=True, null=True)
#     createdate = models.DateField(db_column='CreateDate', blank=True, null=True)
#     onlinedate = models.DateField(db_column='OnlineDate', blank=True, null=True)
#     offlinedate = models.DateField(db_column='OfflineDate', blank=True, null=True)
#     company = models.CharField(db_column='Company', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'App_Platform_cfg'
#
#
# class AppQueryCfg(models.Model):
#     idx = models.AutoField()
#     queryuser = models.CharField(db_column='QueryUser', max_length=50, blank=True, null=True)
#     querypass = models.CharField(db_column='QueryPass', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'App_Query_Cfg'
#         unique_together = (('querypass', 'queryuser'),)
#
#
# class AppServerChannel(models.Model):
#     id = models.AutoField()
#     gid = models.IntegerField(db_column='GID')
#     zoneidx = models.IntegerField()
#     zonename = models.CharField(max_length=50, blank=True, null=True)
#     cid = models.IntegerField(db_column='CID')
#     appid = models.CharField(max_length=50, blank=True, null=True)
#     statu = models.IntegerField()
#     server_statu = models.IntegerField()
#     server_suggest = models.IntegerField()
#     is_delete = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'App_Server_Channel'
#
#
# class AppServerPt(models.Model):
#     id = models.AutoField()
#     gid = models.IntegerField(db_column='GID')
#     zoneidx = models.IntegerField()
#     zonename = models.CharField(max_length=50, blank=True, null=True)
#     pid = models.IntegerField(db_column='PID')
#     statu = models.IntegerField()
#     server_statu = models.IntegerField()
#     server_suggest = models.IntegerField()
#     is_delete = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'App_Server_Pt'
#
#
# class AppVersionList(models.Model):
#     vid = models.IntegerField(db_column='VID')
#     vname = models.CharField(db_column='VName', max_length=50, blank=True, null=True)
#     vinfo = models.CharField(db_column='VInfo', max_length=512, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'App_Version_list'


# class Channel(models.Model):
#     channelid = models.AutoField(db_column='ChannelId')
#     channelname = models.CharField(db_column='ChannelName', max_length=50, blank=True, null=True)
#     projectid = models.IntegerField(db_column='ProjectId', blank=True, null=True)
#     platformid = models.IntegerField(db_column='PlatformId', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Channel'
#
#
# class Checklogin(models.Model):
#     idx = models.AutoField()
#     username = models.CharField(db_column='userName', max_length=50)
#     password = models.CharField(max_length=50)
#     competence = models.CharField(db_column='Competence', max_length=500, blank=True, null=True)
#     pt = models.CharField(max_length=500, blank=True, null=True)
#     gametype = models.CharField(max_length=50, blank=True, null=True)
#     idip = models.IntegerField(db_column='IDIP', blank=True, null=True)
#     user = models.CharField(db_column='User', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'CheckLogin'
#
#
# class DevIdcList(models.Model):
#     idc_id = models.AutoField(db_column='IDC_id')
#     idc_name = models.CharField(db_column='IDC_name', max_length=50, blank=True, null=True)
#     idc_locate = models.CharField(db_column='IDC_Locate', max_length=50, blank=True, null=True)
#     idc_desc = models.CharField(db_column='IDC_Desc', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Dev_IDC_list'
#
#
# class Gamemanagerlogin(models.Model):
#     id = models.AutoField()
#     loginname = models.CharField(db_column='LoginName', max_length=50, blank=True, null=True)
#     loginpass = models.CharField(db_column='LoginPass', max_length=50, blank=True, null=True)
#     ipaddress = models.CharField(db_column='IpAddress', max_length=128, blank=True, null=True)
#     gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True)
#     gametypeno = models.IntegerField(db_column='GameTypeNo', blank=True, null=True)
#     ptarray = models.CharField(db_column='PtArray', max_length=1024, blank=True, null=True)
#     level = models.IntegerField(db_column='Level', blank=True, null=True)
#     lock = models.IntegerField(db_column='Lock', blank=True, null=True)
#     token = models.CharField(max_length=32, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'GameManagerLogin'
#
#
# class GameList(models.Model):
#     game_id = models.IntegerField(db_column='Game_id')
#     game_name = models.CharField(db_column='Game_name', max_length=50)
#     game_stauts = models.SmallIntegerField(db_column='Game_stauts', blank=True, null=True)
#     game_start = models.DateField(db_column='Game_Start', blank=True, null=True)
#     game_end = models.DateField(db_column='Game_end', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Game_list'
#
#
# class Logininfo(models.Model):
#     id = models.AutoField()
#     loginname = models.CharField(db_column='LoginName', max_length=50)
#     loginpass = models.CharField(db_column='LoginPass', max_length=50, blank=True, null=True)
#     ipaddress = models.CharField(db_column='IpAddress', max_length=128, blank=True, null=True)
#     gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True)
#     gametypeno = models.IntegerField(db_column='GameTypeNo', blank=True, null=True)
#     level = models.IntegerField(db_column='Level', blank=True, null=True)
#     lock = models.IntegerField(db_column='Lock', blank=True, null=True)
#     token = models.CharField(max_length=32, blank=True, null=True)
#     svrver = models.IntegerField(db_column='SvrVer', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'LoginInfo'
#
#
# class LogininfoNew(models.Model):
#     id = models.AutoField()
#     loginname = models.CharField(db_column='LoginName', max_length=50)
#     loginpass = models.CharField(db_column='LoginPass', max_length=50, blank=True, null=True)
#     ipaddress = models.CharField(db_column='IpAddress', max_length=128, blank=True, null=True)
#     gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True)
#     gametypeno = models.IntegerField(db_column='GameTypeNo', blank=True, null=True)
#     level = models.IntegerField(db_column='Level', blank=True, null=True)
#     lock = models.IntegerField(db_column='Lock', blank=True, null=True)
#     token = models.CharField(max_length=32, blank=True, null=True)
#     svrver = models.IntegerField(db_column='SvrVer', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'LoginInfo_new'
#
#
# class Platform(models.Model):
#     idx = models.AutoField()
#     platformid = models.IntegerField(db_column='PlatformId', blank=True, null=True)
#     platformname = models.CharField(db_column='PlatformName', max_length=10, blank=True, null=True)
#     platformshotname = models.CharField(db_column='PlatformShotName', max_length=10, blank=True, null=True)
#     projectid = models.IntegerField(db_column='ProjectId', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Platform'
#         unique_together = (('platformid', 'projectid'),)
#
#
# class PlatfromList(models.Model):
#     platform_id = models.IntegerField(db_column='Platform_id', blank=True, null=True)
#     game_id = models.IntegerField(db_column='Game_id', blank=True, null=True)
#     platform_name = models.CharField(db_column='Platform_name', max_length=50, blank=True, null=True)
#     platform_start = models.DateField(db_column='Platform_start', blank=True, null=True)
#     platform_end = models.DateField(db_column='Platform_end', blank=True, null=True)
#     platfrom_status = models.SmallIntegerField(db_column='Platfrom_status', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Platfrom_list'
#
#
# class Project(models.Model):
#     projectid = models.IntegerField(db_column='ProjectId', primary_key=True)
#     projectname = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)
#     projectype = models.IntegerField(db_column='ProjecType', blank=True, null=True)
#     createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)
#     testdate = models.DateTimeField(db_column='TestDate', blank=True, null=True)
#     onlinedate = models.DateTimeField(db_column='OnlineDate', blank=True, null=True)
#     offlinedate = models.DateTimeField(db_column='OfflineDate', blank=True, null=True)
#     supervisor = models.CharField(db_column='Supervisor', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Project'
#
#
# class RdcLogin(models.Model):
#     username = models.CharField(max_length=50, blank=True, null=True)
#     password = models.CharField(max_length=50, blank=True, null=True)
#     rightgroup = models.CharField(max_length=500, blank=True, null=True)
#     ptarray = models.TextField(db_column='PtArray', blank=True, null=True)   This field type is a guess.
#     idarray = models.TextField(db_column='IdArray', blank=True, null=True)   This field type is a guess.
#     ipadd = models.CharField(max_length=50, blank=True, null=True)
#     mac = models.CharField(max_length=50, blank=True, null=True)
#     delete = models.IntegerField(blank=True, null=True)
#     info = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'RDC_Login'
#
#
# class ServerPidTable(models.Model):
#     gametypeno = models.IntegerField(blank=True, null=True)
#     gametype = models.CharField(max_length=20, blank=True, null=True)
#     login = models.TextField(blank=True, null=True)
#     loginkefu = models.TextField(blank=True, null=True)
#     pid = models.IntegerField()
#     pidname = models.CharField(max_length=50, blank=True, null=True)
#     simplepidname = models.CharField(max_length=50, blank=True, null=True)
#     checknameip = models.CharField(max_length=50, blank=True, null=True)
#     checkdbpwd = models.CharField(max_length=50, blank=True, null=True)
#     checknameport = models.IntegerField(blank=True, null=True)
#     txappmissionport = models.IntegerField(db_column='txAppMissionport', blank=True, null=True)
#     globalsvrip = models.CharField(max_length=15, blank=True, null=True)
#     globalport = models.IntegerField(blank=True, null=True)
#     globalportkuafu = models.IntegerField(blank=True, null=True)
#     extendlogip = models.CharField(max_length=15, blank=True, null=True)
#     extendslogport = models.IntegerField(blank=True, null=True)
#     dbname = models.CharField(max_length=50, blank=True, null=True)
#     startzoneid = models.IntegerField(blank=True, null=True)
#     stratgamelogport = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Server_pid_table'


# class ServerTableBakDelete(models.Model):
#     idx = models.AutoField()
#     zonename = models.CharField(db_column='ZoneName', max_length=1024, blank=True, null=True)
#     zoneid = models.IntegerField(db_column='ZoneId', blank=True, null=True)
#     ptid = models.IntegerField(db_column='Ptid', blank=True, null=True)
#     ptname = models.CharField(db_column='PtName', max_length=20, blank=True, null=True)
#     svrid = models.CharField(db_column='SvrId', max_length=50, blank=True, null=True)
#     svrtype = models.CharField(db_column='SvrType', max_length=20, blank=True, null=True)
#     gametypeno = models.IntegerField(db_column='GameTypeno')
#     gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True)
#     ipadd = models.CharField(db_column='IpAdd', max_length=30, blank=True, null=True)
#     dev_id = models.IntegerField(db_column='Dev_id', blank=True, null=True)
#     domainname = models.CharField(db_column='DomainName', max_length=50, blank=True, null=True)
#     h_s_info = models.CharField(db_column='H&S_info', max_length=50, blank=True, null=True)   Field renamed to remove unsuitable characters.
#     servermanagerport = models.IntegerField(db_column='ServermanagerPort', blank=True, null=True)
#     lock = models.IntegerField(db_column='Lock', blank=True, null=True)
#     prostat = models.IntegerField(blank=True, null=True)
#     logzoneid = models.IntegerField(db_column='LogZoneId', blank=True, null=True)
#     logsvrip_in = models.CharField(db_column='LogSvrIp_in', max_length=30, blank=True, null=True)
#     logdb_in = models.CharField(db_column='LogDB_in', max_length=50, blank=True, null=True)
#     loguid_in = models.CharField(db_column='LogUid_in', max_length=50, blank=True, null=True)
#     logpwd_in = models.CharField(db_column='LogPwd_in', max_length=50, blank=True, null=True)
#     logsvrip_out = models.CharField(db_column='LogSvrIp_out', max_length=30, blank=True, null=True)
#     logdb_out = models.CharField(db_column='LogDB_out', max_length=50, blank=True, null=True)
#     loguid_out = models.CharField(db_column='LogUid_out', max_length=50, blank=True, null=True)
#     logpwd_out = models.CharField(db_column='LogPwd_out', max_length=50, blank=True, null=True)
#     hequ = models.CharField(db_column='HeQu', max_length=50, blank=True, null=True)
#     kaiqu_time = models.CharField(max_length=50, blank=True, null=True)
#     hequid = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Server_table-bak_delete'
#
#
# class ServerTable1Delete(models.Model):
#     area_id = models.AutoField(db_column='Area_id', primary_key=True)
#     zonename = models.CharField(db_column='ZoneName', max_length=1024, blank=True, null=True)
#     zoneid = models.IntegerField(db_column='ZoneId', blank=True, null=True)
#     ptid = models.IntegerField(db_column='Ptid', blank=True, null=True)
#     ptname = models.CharField(db_column='PtName', max_length=20, blank=True, null=True)
#     svrid = models.CharField(db_column='SvrId', max_length=50, blank=True, null=True)
#     svrtype = models.CharField(db_column='SvrType', max_length=20, blank=True, null=True)
#     gametypeno = models.IntegerField(db_column='GameTypeno')
#     gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True)
#     ipadd = models.CharField(db_column='IpAdd', max_length=30, blank=True, null=True)
#     domainname = models.CharField(db_column='DomainName', max_length=50, blank=True, null=True)
#     h_s_info = models.CharField(db_column='H&S_info', max_length=50, blank=True, null=True)   Field renamed to remove unsuitable characters.
#     servermanagerport = models.IntegerField(db_column='ServermanagerPort', blank=True, null=True)
#     lock = models.IntegerField(db_column='Lock', blank=True, null=True)
#     prostat = models.IntegerField(blank=True, null=True)
#     logzoneid = models.IntegerField(db_column='LogZoneId', blank=True, null=True)
#     logsvrip_in = models.CharField(db_column='LogSvrIp_in', max_length=30, blank=True, null=True)
#     logdb_in = models.CharField(db_column='LogDB_in', max_length=50, blank=True, null=True)
#     loguid_in = models.CharField(db_column='LogUid_in', max_length=50, blank=True, null=True)
#     logpwd_in = models.CharField(db_column='LogPwd_in', max_length=50, blank=True, null=True)
#     logsvrip_out = models.CharField(db_column='LogSvrIp_out', max_length=30, blank=True, null=True)
#     logdb_out = models.CharField(db_column='LogDB_out', max_length=50, blank=True, null=True)
#     loguid_out = models.CharField(db_column='LogUid_out', max_length=50, blank=True, null=True)
#     logpwd_out = models.CharField(db_column='LogPwd_out', max_length=50, blank=True, null=True)
#     hequ = models.CharField(db_column='HeQu', max_length=50, blank=True, null=True)
#     kaiqu_time = models.CharField(max_length=50, blank=True, null=True)
#     hequid = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Server_table_1_delete'
#
#
# class ServerTableBak(models.Model):
#     idx = models.AutoField()
#     zonename = models.CharField(db_column='ZoneName', max_length=1024, blank=True, null=True)
#     zoneid = models.IntegerField(db_column='ZoneId', blank=True, null=True)
#     ptid = models.IntegerField(db_column='Ptid', blank=True, null=True)
#     ptname = models.CharField(db_column='PtName', max_length=20, blank=True, null=True)
#     svrid = models.CharField(db_column='SvrId', max_length=50, blank=True, null=True)
#     svrtype = models.CharField(db_column='SvrType', max_length=20, blank=True, null=True)
#     gametypeno = models.IntegerField(db_column='GameTypeno')
#     gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True)
#     ipadd = models.CharField(db_column='IpAdd', max_length=30, blank=True, null=True)
#     dev_id = models.IntegerField(db_column='Dev_id', blank=True, null=True)
#     domainname = models.CharField(db_column='DomainName', max_length=50, blank=True, null=True)
#     h_s_info = models.CharField(db_column='H&S_info', max_length=50, blank=True, null=True)   Field renamed to remove unsuitable characters.
#     servermanagerport = models.IntegerField(db_column='ServermanagerPort', blank=True, null=True)
#     lock = models.IntegerField(db_column='Lock', blank=True, null=True)
#     prostat = models.IntegerField(blank=True, null=True)
#     logzoneid = models.IntegerField(db_column='LogZoneId', blank=True, null=True)
#     logsvrip_in = models.CharField(db_column='LogSvrIp_in', max_length=30, blank=True, null=True)
#     logdb_in = models.CharField(db_column='LogDB_in', max_length=50, blank=True, null=True)
#     loguid_in = models.CharField(db_column='LogUid_in', max_length=50, blank=True, null=True)
#     logpwd_in = models.CharField(db_column='LogPwd_in', max_length=50, blank=True, null=True)
#     logsvrip_out = models.CharField(db_column='LogSvrIp_out', max_length=30, blank=True, null=True)
#     logdb_out = models.CharField(db_column='LogDB_out', max_length=50, blank=True, null=True)
#     loguid_out = models.CharField(db_column='LogUid_out', max_length=50, blank=True, null=True)
#     logpwd_out = models.CharField(db_column='LogPwd_out', max_length=50, blank=True, null=True)
#     hequ = models.CharField(db_column='HeQu', max_length=50, blank=True, null=True)
#     kaiqu_time = models.CharField(max_length=50, blank=True, null=True)
#     hequid = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Server_table_bak'
#
#
# class Weblogin(models.Model):
#     idx = models.AutoField()
#     username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)
#     password = models.CharField(db_column='Password', max_length=50, blank=True, null=True)
#     appid = models.IntegerField(db_column='Appid', blank=True, null=True)
#     platformid = models.IntegerField(db_column='Platformid', blank=True, null=True)
#     powerid = models.CharField(db_column='Powerid', max_length=50, blank=True, null=True)
#     type = models.IntegerField(blank=True, null=True)
#     name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'WebLogin'
#
#
# class Aatmp(models.Model):
#     id = models.AutoField()
#     sid = models.IntegerField(db_column='SID', blank=True, null=True)
#     sname = models.CharField(db_column='SName', max_length=512, blank=True, null=True)
#     pid = models.IntegerField(db_column='PID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     apid = models.IntegerField(db_column='APID', blank=True, null=True)
#     display = models.IntegerField(db_column='Display', blank=True, null=True)
#     devid = models.IntegerField(db_column='DevID', blank=True, null=True)
#     dn = models.CharField(db_column='DN', max_length=50, blank=True, null=True)
#     vid = models.IntegerField(db_column='VID', blank=True, null=True)
#     type = models.IntegerField(db_column='Type', blank=True, null=True)
#     status = models.IntegerField(db_column='Status', blank=True, null=True)
#     prostatus = models.IntegerField(db_column='ProStatus', blank=True, null=True)
#     opendate = models.DateField(db_column='OpenDate', blank=True, null=True)
#     mergedate = models.DateField(db_column='MergeDate', blank=True, null=True)
#     mergeid = models.IntegerField(db_column='MergeID', blank=True, null=True)
#     mergeidx = models.IntegerField(db_column='MergeIdx', blank=True, null=True)
#     serverid = models.IntegerField(db_column='ServerID', blank=True, null=True)
#     gslist = models.CharField(db_column='GSList', max_length=50, blank=True, null=True)
#     dbsvr_in = models.CharField(db_column='DBSvr_in', max_length=50, blank=True, null=True)
#     dbname_in = models.CharField(db_column='DBName_in', max_length=50, blank=True, null=True)
#     dbqueryid_in = models.IntegerField(db_column='DBQueryId_in', blank=True, null=True)
#     dbsvr_out = models.CharField(db_column='DBSvr_out', max_length=50, blank=True, null=True)
#     dbname_out = models.CharField(db_column='DBName_out', max_length=50, blank=True, null=True)
#     dbqueryid_out = models.IntegerField(db_column='DBQueryId_out', blank=True, null=True)
#     serverpath = models.CharField(db_column='ServerPath', max_length=50, blank=True, null=True)
#     smport = models.IntegerField(db_column='SMPort', blank=True, null=True)
#     loginport = models.CharField(db_column='LoginPort', max_length=50, blank=True, null=True)
#     rmbport = models.IntegerField(db_column='RmbPort', blank=True, null=True)
#     db_svrcfg = models.CharField(max_length=50, blank=True, null=True)
#     db_player = models.CharField(max_length=50, blank=True, null=True)
#     db_login = models.CharField(max_length=50, blank=True, null=True)
#     db_super = models.CharField(max_length=50, blank=True, null=True)
#     db_rmb = models.CharField(max_length=50, blank=True, null=True)
#     db_param = models.CharField(max_length=50, blank=True, null=True)
#     trigger_flag = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'aatmp'
#
#
# class Apk(models.Model):
#     idx = models.AutoField()
#     apkid = models.CharField(db_column='apkId', max_length=128, blank=True, null=True)
#     apkname = models.CharField(db_column='apkName', max_length=50, blank=True, null=True)
#     parentchannelid = models.IntegerField(db_column='parentChannelId', blank=True, null=True)
#     parentprojectid = models.IntegerField(db_column='parentProjectId', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'apk'
#         unique_together = (('parentchannelid', 'apkid', 'parentprojectid'),)
#
#
# class CfgAppInfo(models.Model):
#     idx = models.IntegerField(blank=True, null=True)
#     appid = models.CharField(max_length=50)
#     appname = models.CharField(max_length=50, blank=True, null=True)
#     subchannelid = models.IntegerField(blank=True, null=True)
#     style = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'cfg_app_info'
#
#
# class CfgSubchannelInfo(models.Model):
#     id = models.IntegerField(blank=True, null=True)
#     subchannel = models.CharField(max_length=50, blank=True, null=True)
#     channelid = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'cfg_subchannel_info'
#
#
# class Devused(models.Model):
#     idx = models.AutoField()
#     logdate = models.DateField()
#     gametypeno = models.IntegerField(blank=True, null=True)
#     ptid = models.IntegerField(blank=True, null=True)
#     lock = models.IntegerField(blank=True, null=True)
#     idcid = models.IntegerField()
#     used = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'devused'
#
#
# class IptableFilter(models.Model):
#     iptabletype = models.AutoField(primary_key=True)
#     filterlistname = models.CharField(max_length=50)
#     action = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'iptable_filter'
#
#
# class IptableGroup(models.Model):
#     groupid = models.AutoField()
#     groupname = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'iptable_group'
#
#
# class IptableGroupRule(models.Model):
#     idx = models.AutoField()
#     groupid = models.IntegerField(blank=True, null=True)
#     ruleid = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'iptable_group_rule'
#
#
# class IptableRuleBak(models.Model):
#     id = models.AutoField()
#     srcaddr = models.CharField(max_length=15, blank=True, null=True)
#     dstaddr = models.CharField(max_length=15, blank=True, null=True)
#     protocol = models.CharField(max_length=50, blank=True, null=True)
#     srcprot = models.CharField(max_length=50, blank=True, null=True)
#     dstport = models.CharField(max_length=50, blank=True, null=True)
#     description = models.CharField(max_length=50, blank=True, null=True)
#     filterlist = models.ForeignKey(IptableFilter, models.DO_NOTHING, db_column='filterlist')
#     info = models.CharField(max_length=256, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'iptable_rule-bak'
#
#
# class IptableRules(models.Model):
#     ip = models.CharField(db_column='IP', max_length=50, blank=True, null=True)
#     protocol = models.CharField(max_length=50, blank=True, null=True)
#     port = models.CharField(max_length=512, blank=True, null=True)
#     des = models.CharField(max_length=50, blank=True, null=True)
#     filterlist = models.ForeignKey(IptableFilter, models.DO_NOTHING, db_column='filterlist', blank=True, null=True)
#     direction = models.IntegerField(blank=True, null=True)
#     info = models.CharField(max_length=512, blank=True, null=True)
#     limitetime = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'iptable_rules'
#
#
# class ServerGmaccount(models.Model):
#     idx = models.AutoField()
#     account = models.CharField(db_column='Account', max_length=50)
#     password = models.CharField(db_column='Password', max_length=50)
#     mac = models.CharField(db_column='Mac', max_length=50, blank=True, null=True)
#     pt = models.TextField(db_column='Pt', blank=True, null=True)
#     ipadd = models.CharField(db_column='Ipadd', max_length=100, blank=True, null=True)
#     gmlvl = models.IntegerField(db_column='Gmlvl', blank=True, null=True)
#     accounttype = models.CharField(db_column='AccountType', max_length=20, blank=True, null=True)
#     gametype = models.CharField(db_column='GameType', max_length=20, blank=True, null=True)
#     gametypeno = models.IntegerField(db_column='GameTypeNo', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'server_gmaccount'
#
#
# class ServerIplistTbl(models.Model):
#     dev_id = models.AutoField(db_column='Dev_id')
#     ct_ipadd = models.CharField(db_column='CT_ipadd', max_length=50)
#     local_ipadd = models.CharField(db_column='Local_ipadd', max_length=50, blank=True, null=True)
#     owner_id = models.IntegerField(blank=True, null=True)
#     idc_id = models.IntegerField(db_column='IDC_id', blank=True, null=True)
#     owner_des = models.CharField(max_length=20, blank=True, null=True)
#     delete = models.IntegerField(blank=True, null=True)
#     admin = models.CharField(max_length=50, blank=True, null=True)
#     password = models.CharField(max_length=50, blank=True, null=True)
#     sqllogin = models.CharField(db_column='SQLLogin', max_length=50, blank=True, null=True)
#     sqlpwd = models.CharField(db_column='SQLPwd', max_length=50, blank=True, null=True)
#     gametype = models.CharField(max_length=20, blank=True, null=True)
#     port = models.IntegerField(blank=True, null=True)
#     console = models.IntegerField(blank=True, null=True)
#     server_on = models.DateField(blank=True, null=True)
#     server_off = models.DateField(blank=True, null=True)
#     location = models.CharField(max_length=20, blank=True, null=True)
#     info = models.TextField(blank=True, null=True)  # This field type is a guess.
#     hardware = models.TextField(blank=True, null=True)  # This field type is a guess.
#     cpu = models.CharField(db_column='CPU', max_length=50, blank=True, null=True)
#     hd = models.CharField(db_column='HD', max_length=50, blank=True, null=True)
#     mem = models.CharField(db_column='MEM', max_length=50, blank=True, null=True)
#     ipsec_group = models.CharField(db_column='IPSec_group', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'server_iplist_tbl'
#
#
# class Subplatform2(models.Model):
#     idx = models.AutoField()
#     subplatformid = models.CharField(db_column='subPlatformId', max_length=50, blank=True, null=True)
#     subplatformname = models.CharField(db_column='subPlatformName', max_length=50, blank=True, null=True)
#     parentchannelid = models.IntegerField(db_column='parentChannelId', blank=True, null=True)
#     parentprojectid = models.IntegerField(db_column='parentProjectId', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'subPlatform2'
#         unique_together = (('parentchannelid', 'subplatformid', 'parentprojectid'),)
#
#
# class Sysdiagrams(models.Model):
#     name = models.CharField(max_length=128)
#     principal_id = models.IntegerField()
#     diagram_id = models.AutoField(primary_key=True)
#     version = models.IntegerField(blank=True, null=True)
#     definition = models.BinaryField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'sysdiagrams'
#         unique_together = (('principal_id', 'name'),)
