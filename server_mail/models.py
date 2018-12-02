from django.db import models


class MailInfo(models.Model):
    ip_address = models.CharField(max_length=15, verbose_name='IP地址')
    title = models.CharField(max_length=20, verbose_name='标题')
    content = models.CharField(max_length=50, verbose_name='内容')
    sent = models.BooleanField(default=False, verbose_name='已发送')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '邮件信息'
        verbose_name_plural = verbose_name

class MailRule(models.Model):
    type = models.CharField(max_length=20, verbose_name='报警类型')
    description = models.CharField(max_length=20, verbose_name='报警描述')
    rule = models.CharField(max_length=20, verbose_name='发送规则')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = '邮件规则'
        verbose_name_plural = verbose_name


class MailOperation(models.Model):
    game = models.CharField(max_length=20, verbose_name='游戏')
    operation_rule = models.ManyToManyField(MailRule, verbose_name='操作规则')
    receiver = models.CharField(max_length=20, verbose_name='收件人')

    def __str__(self):
        return self.game + '_' + self.operation_rule

    class Meta:
        verbose_name = '邮件操作'
        verbose_name_plural = verbose_name