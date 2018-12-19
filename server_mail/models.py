import os
from django.db import models


class SendRule(models.Model):
    rule = models.CharField(max_length=20, verbose_name='发送规则')
    description = models.CharField(max_length=50, verbose_name='规则描述')

    def __str__(self):
        return self.rule

    class Meta:
        verbose_name = '发送规则'
        verbose_name_plural = verbose_name


class AlarmRule(models.Model):
    alarm_type = models.CharField(max_length=20, verbose_name='报警类型')
    description = models.CharField(max_length=20, verbose_name='报警描述')
    json_args = models.CharField(max_length=50, verbose_name='前端参数', default='')
    template_kwargs = models.CharField(max_length=50, verbose_name='模板参数', default='')
    send_rules = models.ForeignKey(SendRule, on_delete=models.SET_NULL, null=True, verbose_name='发送规则')


    def __str__(self):
        return self.description

    class Meta:
        verbose_name = '邮件规则'
        verbose_name_plural = verbose_name


class MailInfo(models.Model):
    ip_address = models.CharField(max_length=15, verbose_name='IP地址', null=True, blank=True)
    game = models.CharField(max_length=20, verbose_name='游戏', null=True, blank=True)
    platform = models.CharField(max_length=20, verbose_name='平台', null=True, blank=True)
    zone = models.CharField(max_length=20, verbose_name='区服', null=True, blank=True)
    title = models.CharField(max_length=20, verbose_name='标题')
    content = models.CharField(max_length=50, verbose_name='内容')
    sent = models.BooleanField(default=False, verbose_name='已发送')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    mail_types = models.ManyToManyField(AlarmRule, verbose_name='邮件类型')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']
        verbose_name = '邮件信息'
        verbose_name_plural = verbose_name


class MailOperation(models.Model):
    game = models.CharField(max_length=20, verbose_name='游戏', null=True, blank=True)
    alarms = models.ManyToManyField(AlarmRule, verbose_name='操作规则')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    send_rules = models.ForeignKey(SendRule, on_delete=models.SET_DEFAULT, null=True, verbose_name='发送规则', default='')

    def __str__(self):
        return self.game + '_' + self.receiver

    def get_game_info(self, data):
        self.ip = data.get('ip', '')
        self.game = data.get('game', '')
        self.platform = data.get('platform', '')
        self.zone = data.get('zone', '')

    class Meta:
        ordering = ['-created_date']
        verbose_name = '邮件操作'
        verbose_name_plural = verbose_name



