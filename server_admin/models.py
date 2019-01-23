# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UserWithEmailManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(emailaddress='').exclude(emailaddress=None)


class WXUser


class User(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True, verbose_name='用户id')
    useridentity = models.CharField(db_column='userIdentity', max_length=50, verbose_name='用户身份')
    password = models.CharField(db_column='passWord', max_length=50, blank=True, null=True, verbose_name='密码')
    emailaddress = models.CharField(db_column='emailAddress', max_length=32, blank=True, null=True, verbose_name='邮件地址')
    # phonenumber = models.CharField(db_column='phoneNumber', max_length=11, blank=True, null=True)
    # ipaddress = models.CharField(db_column='ipAddress', max_length=16, blank=True, null=True)
    # mac = models.CharField(max_length=32, blank=True, null=True)
    # username = models.CharField(db_column='userName', max_length=50, blank=True, null=True)
    # admin = models.IntegerField(blank=True, null=True)
    # failcount = models.IntegerField(db_column='failCount', blank=True, null=True)
    # lastlogintime = models.IntegerField(db_column='lastLoginTime', blank=True, null=True)
    # token = models.CharField(max_length=32, blank=True, null=True)

    objects = UserWithEmailManager()

    def __str__(self):
        return self.useridentity

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        app_label = 'server_admin'
        managed = False
        db_table = 'User'


# class Appid(models.Model):
#     idx = models.AutoField()
#     gameid = models.IntegerField()
#     appid = models.CharField(max_length=50)
#     channelid = models.IntegerField(db_column='channelId')
#
#     class Meta:
#         managed = False
#         db_table = 'Appid'
#
#
# class Mvcmenu(models.Model):
#     name = models.CharField(max_length=50)
#     parentid = models.IntegerField(blank=True, null=True)
#     functionid = models.IntegerField(db_column='functionId', blank=True, null=True)
#     m = models.CharField(max_length=20, blank=True, null=True)
#     c = models.CharField(max_length=20, blank=True, null=True)
#     a = models.CharField(max_length=20, blank=True, null=True)
#     listorder = models.IntegerField(db_column='listOrder', blank=True, null=True)
#     display = models.SmallIntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'MVCmenu'
#
#
# class Role(models.Model):
#     roleid = models.AutoField(db_column='roleID')
#     systemid = models.IntegerField(db_column='systemID', blank=True, null=True)
#     rolename = models.CharField(db_column='roleName', max_length=128, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Role'
#
#
# class System(models.Model):
#     systemid = models.AutoField(db_column='systemId')
#     systemname = models.CharField(db_column='systemName', max_length=50, blank=True, null=True)
#     info = models.CharField(max_length=10, blank=True, null=True)
#     systemlvl = models.IntegerField(db_column='systemLvl', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'System'
#
#
# class Urapgf(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     rid = models.IntegerField(db_column='RID', blank=True, null=True)
#     aid = models.IntegerField(db_column='AID', blank=True, null=True)
#     pid = models.IntegerField(db_column='PID', blank=True, null=True)
#     sid = models.IntegerField(db_column='SID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     fid = models.IntegerField(db_column='FID', blank=True, null=True)
#     cid = models.IntegerField(db_column='CID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'URAPGF'
#
#
# class UrgfDel(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     rid = models.IntegerField(db_column='RID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     fid = models.IntegerField(db_column='FID', blank=True, null=True)
#     sid = models.IntegerField(db_column='SID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'URGF-del'
#
#

#
#
# class Function(models.Model):
#     functionid = models.AutoField(db_column='functionId', primary_key=True)
#     systemid = models.IntegerField(db_column='systemId', blank=True, null=True)
#     functiondescription = models.CharField(db_column='functionDescription', max_length=512, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'function'
#
#
# class G2F(models.Model):
#     idx = models.AutoField()
#     groupid = models.IntegerField(db_column='GroupId', blank=True, null=True)
#     functionid = models.IntegerField(db_column='FunctionId', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'g2f'
#
#
# class Group(models.Model):
#     groupid = models.AutoField(db_column='groupId', primary_key=True)
#     systemid = models.IntegerField(db_column='systemId', blank=True, null=True)
#     groupname = models.CharField(db_column='groupName', max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'group'
#
#
# class S1AAuthority(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     fid = models.IntegerField(db_column='FID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 's1_A_authority'
#
#
# class S1PAuthority(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     projid = models.IntegerField(db_column='ProjId', blank=True, null=True)
#     platid = models.IntegerField(db_column='PlatId', blank=True, null=True)
#     type = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 's1_P_authority'
#
#
# class S2AAuthority(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     fid = models.IntegerField(db_column='FID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 's2_A_authority'
#
#
# class S2PAuthority(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     projid = models.IntegerField(db_column='ProjId', blank=True, null=True)
#     platid = models.IntegerField(db_column='PlatId', blank=True, null=True)
#     type = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 's2_P_authority'
#
#
# class S3AAuthority(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     rid = models.IntegerField(db_column='RID', blank=True, null=True)
#     gid = models.IntegerField(db_column='GID', blank=True, null=True)
#     fid = models.IntegerField(db_column='FID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 's3_A_authority'
#
#
# class S3PAuthority(models.Model):
#     idx = models.AutoField()
#     uid = models.IntegerField(db_column='UID', blank=True, null=True)
#     projid = models.IntegerField(db_column='ProjId', blank=True, null=True)
#     platid = models.IntegerField(db_column='PlatId', blank=True, null=True)
#     type = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 's3_P_authority'
#
#
# class S3RAuthority(models.Model):
#     idx = models.AutoField()
#     roleid = models.IntegerField(db_column='roleID', blank=True, null=True)
#     userid = models.IntegerField(db_column='userID', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 's3_R_authority'
