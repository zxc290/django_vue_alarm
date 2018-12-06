from django.db import models


class AlarmRule(models.Model):
    alarm_type = models.CharField(max_length=20, verbose_name='报警类型')
    description = models.CharField(max_length=20, verbose_name='报警描述')
    alarm_rule = models.CharField(max_length=20, verbose_name='发送规则')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = '邮件规则'
        verbose_name_plural = verbose_name


class MailInfo(models.Model):
    ip_address = models.CharField(max_length=15, verbose_name='IP地址')
    game = models.CharField(max_length=20, verbose_name='游戏')
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
    game = models.CharField(max_length=20, verbose_name='游戏')
    alarms = models.ManyToManyField(AlarmRule, verbose_name='操作规则')
    receiver = models.CharField(max_length=20, verbose_name='收件人')

    def __str__(self):
        return self.game + '_' + self.alarms

    class Meta:
        verbose_name = '邮件操作'
        verbose_name_plural = verbose_name



