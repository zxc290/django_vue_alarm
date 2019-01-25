# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppList(models.Model):
    gid = models.IntegerField(db_column='GID', primary_key=True)  # Field name made lowercase.
    gname = models.CharField(db_column='GName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gtype = models.IntegerField(db_column='GType', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    testdate = models.DateField(db_column='TestDate', blank=True, null=True)  # Field name made lowercase.
    onlinedate = models.DateField(db_column='OnlineDate', blank=True, null=True)  # Field name made lowercase.
    offlinedate = models.DateField(db_column='OfflineDate', blank=True, null=True)  # Field name made lowercase.
    supervisor = models.CharField(db_column='Supervisor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sendruleid = models.IntegerField(db_column='SendRuleId', blank=True, null=True)  # Field name made lowercase.
    alarmruleid = models.IntegerField(db_column='AlarmRuleId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'App_list'
