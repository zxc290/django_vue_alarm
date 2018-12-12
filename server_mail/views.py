import json
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MailInfo, AlarmRule, MailOperation
from .serializers import MailInfoSerializer, AlarmRuleSerializer, MailOperationSerializer
from server_management.models import ServerTable
from server_admin.models import User
from .mail_distribute import *
from . import scheduler
from datetime import datetime, timedelta
from .send_mail import async_send_mail


class MailInfoViewSet(viewsets.ModelViewSet):
    queryset = MailInfo.objects.all()
    serializer_class = MailInfoSerializer


class AlarmRuleViewSet(viewsets.ModelViewSet):
    queryset = AlarmRule.objects.all()
    serializer_class = AlarmRuleSerializer


class MailOperationViewSet(viewsets.ModelViewSet):
    queryset = MailOperation.objects.all()
    serializer_class = MailOperationSerializer


@api_view(['POST'])
def deal_alarm(request):
    data = json.loads(request.body)
    print(data)
    # 报警类型
    alarm_type = data.get('type')
    # 当前报警类型的游戏的邮件类实例化
    mail_instance = alarm_hash[alarm_type](data)
    # 验证前端json参数
    if mail_instance.validate_json_data(*mail_instance.json_args):
        # 获取邮件主题和内容
        subject, content = mail_instance.generate_subject_and_message(**mail_instance.txt_kwargs)
        # 报警规则对象
        alarm_rule = mail_instance.alarm_rule
        # 报警邮件发送规则
        mail_rule = alarm_rule.alarm_rule
        receiver_mail_list = mail_instance.get_reciever_mail_list(alarm_type)
        # 保存邮件信息
        mail_info = MailInfo.objects.create(ip_address=mail_instance.ip, game=mail_instance.gametype, title=subject.split(']')[0].strip('['),
                                            content=content)
        mail_info.mail_types.add(alarm_rule)
        # 定义发送邮件参数，传入实例方便修改状态
        mail_info_args = [mail_info, ]
        mail_info_kwargs = {
            'subject': subject,
            'message': content,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': ['290704731@qq.com'],
            'fail_silently': False,
        }

        if mail_rule == '即时':
            old_mail = MailInfo.objects.filter(game=mail_instance.gametype).filter(mail_types=alarm_rule).filter(sent=True).first()
            # 不存在旧邮件，直接发
            if not old_mail:
                async_send_mail(*mail_info_args, **mail_info_kwargs)

            # 存在旧邮件，比较时间差是否大于1小时
            else:
                timedelta_seconds = (mail_info.create_date - old_mail.create_date).seconds
                timedelta_hours = timedelta_seconds // 3600
                if timedelta_hours >= 1:
                    async_send_mail(*mail_info_args, **mail_info_kwargs)

        elif mail_rule == '定时9,17点':
            date = datetime.now()
            today_start = date.replace(hour=0, minute=0, second=0)
            tomorrow_start = today_start + timedelta(days=1)
            hour = date.hour
            if hour == 9 or 17:
                old_mail = MailInfo.objects.filter(game=mail_instance.gametype).filter(mail_types=alarm_rule).filter(sent=True).filter(
                    create_date__range=[today_start, tomorrow_start]).first()
                # 今天无此游戏报警的邮件，直接发
                if not old_mail:
                    async_send_mail(*mail_info_args, **mail_info_kwargs)
                else:
                    # 今天有此类游戏的报警,但不是这个时间点的，直接发
                    if old_mail.create_date.hour != hour:
                        async_send_mail(*mail_info_args, **mail_info_kwargs)

        elif mail_rule == '积累1小时':
            date = datetime.now()
            # 下个小时的整点发
            run_date = datetime(date.year, date.month, date.day, date.hour) + timedelta(hours=1)
            job_id = mail_instance.gametype + '_' + alarm_type + '_' + str(run_date.hour)

            # 根据任务id获取任务
            sched = scheduler.get_job(job_id)
            # 如果有任务存在，追加邮件内容，追加邮件信息实例
            if sched:
                modified_content = sched.kwargs.get('message') + '\r\n\r\n' + content
                mail_info_args.append(mail_info)
                mail_info_kwargs['message'] = modified_content
                sched.modify(args=mail_info_args, kwargs=mail_info_kwargs)
            # 如果任务不存在，新增定时任务
            else:
                scheduler.add_job(
                    func=async_send_mail, trigger='date', run_date=run_date, id=job_id,
                    args=mail_info_args, kwargs=mail_info_kwargs
                )
        return JsonResponse({'code': 1, 'message': '成功'})
    else:
        return JsonResponse({'code': 0, 'message': '参数错误'})


@api_view(['GET', 'POST'])
def test(request):
    print(json.loads(request.body))
    d = {'message':'test'}
    return JsonResponse(d)


@api_view(['POST'])
def add_rule(request):
    data = json.loads(request.body).get('params')
    alarm_description = data.get('alarmType')
    game = data.get('game')
    receiver = data.get('receiver')
    mail_operation = MailOperation.objects.create(game=game, receiver=receiver)
    alarm_rule = AlarmRule.objects.filter(description=alarm_description).first()
    alarm_rule.mailoperation_set.add(mail_operation)
    alarm_rule.save()
    msg = {'code':1, 'message': '成功'}
    return JsonResponse(msg)


@api_view(['POST'])
def delete_rule(request):
    data = json.loads(request.body)
    alarm_id = data.get('alarmId')
    alarm_rule = AlarmRule.objects.get(id=alarm_id)
    mail_operation_id_list = data.get('delArr')
    mail_operation_list = [MailOperation.objects.get(id=each) for each in mail_operation_id_list]
    for mail_operation in mail_operation_list:
        mail_operation.alarms.remove(alarm_rule)
        mail_operation.delete()
    # game = data.get('game')
    # receiver = data.get('receiver')
    # alarm_id = data.get('alarmId')
    # alarm_rule = AlarmRule.objects.get(id=alarm_id)
    # mail_operation = MailOperation.objects.filter(game=game, receiver=receiver).first()
    # alarm_rule.mailoperation_set.remove(mail_operation)
    # mail_operation.delete()
    msg = {'code': 1, 'message': '成功'}
    return JsonResponse(msg)


def index(request):
    return render(request, '../frontend/index.html')