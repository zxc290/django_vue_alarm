import json
from django.core.mail import send_mail
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
from apscheduler.schedulers.background import BackgroundScheduler
from . import scheduler
from datetime import datetime, timedelta
from .send_mail import async_send_mail


# from .aps_tasks import send_mail_by_hour


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
    # ip地址
    # ip = data.get('ip')
    # 报警类型
    alarm_type = data.get('type')
    print(alarm_type)
    # 报警服务器
    # server = ServerTable.objects.filter(ipadd=ip).first()
    # 报警服务器当下游戏
    # game = server.gametype
    # 报警规则对象
    # alarm_rule = AlarmRule.objects.filter(alarm_type=alarm_type).first()
    # 报警邮件发送规则
    # mail_rule = alarm_rule.alarm_rule
    # print(mail_rule)
    # 当前报警类型的游戏的负责人姓名列表
    # receiver_name_list = MailOperation.objects.filter(game=game).filter(alarms=alarm_rule).all()
    # 上述姓名列表获取用户对象列表的邮件列表
    # receiver_mail_list = [User.objects.filter(useridentity=name).first().emailaddress for name in receiver_name_list]
    # 当前报警类型的游戏的邮件类实例化
    mail_instance = alarm_hash[alarm_type](data)
    # 验证前端json参数
    print(mail_instance.validate_json_data(*mail_instance.json_args))
    if mail_instance.validate_json_data(*mail_instance.json_args):
        print(mail_instance.json_args)
        # return JsonResponse({'code': 0, 'message': '参数错误'})
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
        # mail_info = MailInfo.objects.create(ip_address=ip, game=game, title=subject.split(']')[0].strip('['), content=content)
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
                return JsonResponse({'code': 1, 'message': '成功'})
            # 存在旧邮件，比较时间差是否大于1小时
            else:
                timedelta_seconds = (mail_info.create_date - old_mail.create_date).seconds
                timedelta_hours = timedelta_seconds // 3600
                if timedelta_hours >= 1:
                    async_send_mail(*mail_info_args, **mail_info_kwargs)
                    return JsonResponse({'code': 1, 'message': '成功'})
            # send_mail(subject=subject, message=content, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['290704731@qq.com'], fail_silently=False)
            # async_send_mail(*mail_info_args, **mail_info_kwargs)
            # # mail_info.sent = True
            # # mail_info.save()
            # return JsonResponse({'code': 1, 'message': '成功'})

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
                    return JsonResponse({'code': 1, 'message': '成功'})
                else:
                    # 今天有此类游戏的报警,但不是这个时间点的，直接发
                    if old_mail.create_date.hour != hour:
                        async_send_mail(*mail_info_args, **mail_info_kwargs)
                        return JsonResponse({'code': 1, 'message': '成功'})

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
        # 当天9点前，9点发
        # if hour < 9:
        #     run_date = datetime(date.year, date.month, date.day, 9)
        #     # a游戏_充值_9
        #     job_id = game + '_' + alarm_type + '_9'
        # # 当天9-17点间， 17点发
        # elif 9 <= hour < 17:
        #     run_date = datetime(date.year, date.month, date.day, 17)
        #     job_id = game + '_' + alarm_type + '_17'
        # # 超过17点，第二天9点发
        # else:
        #     run_date = datetime(date.year, date.month, date.day, 9) + timedelta(days=1)
        #     job_id = game + '_' + alarm_type + '_9'
        #
        # # 根据任务id获取任务
        # sched = scheduler.get_job(job_id)
        # # 如果有任务存在，新邮件覆盖旧邮件，旧邮件存数据库，sent=False，新邮件存数据库，sent=True
        # if sched:
        #     sched.modify(args=mail_info_args, kwargs=mail_info_kwargs)
        # # 如果任务不存在，新增定时任务
        # else:
        #     scheduler.add_job(
        #         func=async_send_mail, trigger='date', run_date=run_date, id=job_id,
        #         args=mail_info_args, kwargs=mail_info_kwargs
        #     )
        # return JsonResponse({'code': 1, 'message': '成功'})
    # wu
    # elif mail_rule == '1小时内不重复':
    #     old_mail = MailInfo.objects.filter(game=game).filter(mail_types=alarm_rule).filter(sent=True).first()
    #     # 不存在旧邮件，直接发
    #     if not old_mail:
    #         async_send_mail(*mail_info_args, **mail_info_kwargs)
    #         return JsonResponse({'code': 1, 'message': '成功'})
    #     # 存在旧邮件，比较时间差是否大于1小时
    #     else:
    #         timedelta_seconds = (mail_info.create_date - old_mail.create_date).seconds
    #         timedelta_hours = timedelta_seconds // 3600
    #         if timedelta_hours >= 1:
    #             async_send_mail(*mail_info_args, **mail_info_kwargs)
    #             return JsonResponse({'code': 1, 'message': '成功'})

    # data = request.get_json()
    # print(data)
    # # 获取ip
    # ip = data.get('ip')
    # # 待数据库
    # server_list = ServerManagement_Session.query(Server).filter_by(IpAdd=ip).all()
    # gametype = server_list[0].GameType
    # # game = Game.query.filter_by(gametype=gametype).first()
    # # if game:
    # # 列表生成式，根据该游戏的管理员的名字查询得到用户对象，获取emailAdddress属性，合成列表
    # # receivers = [ServerAdmin_Session.query(User).filter_by(userIdentity=receiver.username).first().emailAddress
    # #              for
    # #              receiver in game.receivers]
    #
    # if server_list:
    #     # 获取邮件类型
    #     _type = data.get('type')
    #     # rule对象
    #     rule = Rule.query.filter_by(type=_type).first()
    #     # rule发送规则
    #     rule_name = rule.rulename
    #     # rule中文
    #     rule_description = rule.description
    #     now = datetime.now()
    #     date = now.date()
    #     # 实例化映射的邮件类型
    #     ins = app.config['MAIL_CLASS'][_type](data, server_list, _type)
    #     # 调用实例方法生成主题和邮件内容
    #     subject, msg = ins.generate_subject_and_message()
    #     # subject, msg = generate_subject_and_message(_type, data, server_list, ip)
    #
    #     # 初始化邮件记录实例
    #     mail = Mail(ip_address=ip, title=subject.split(']')[0] + ']', message=msg)
    #
    #     # 收件人姓名列表
    #     receiver_list = [each.receiver for each in
    #                      Manage.query.filter_by(game=gametype).filter_by(rule=rule_description).all()]
    #     # 收件人邮箱列表
    #     email_list = [ServerAdmin_Session.query(User).filter_by(userIdentity=each).first().emailAddress for each in
    #                   receiver_list]
    #     print(email_list)
    #
    #     if rule_name == '即时':
    #         send_email(subject, ['290704731@qq.com'], msg)
    #         mail.sent = True
    #         db.session.add(mail)
    #         db.session.commit()
    #         return {'code': 1, 'message': '成功'}
    #     elif rule_name == '定时9,17点':
    #         # 只处理9点或17点的请求
    #         if now.hour == 9 or 17:
    #             # 如果是不是当天的请求，不会有此时的记录，必发邮件，此时是新的一天的第一个请求
    #             if date not in in_time_alarm:
    #                 # 清空前一天的字典
    #                 in_time_alarm.clear()
    #                 # 初始化字典嵌套字典
    #                 in_time_alarm[date] = {ip: now.hour}
    #                 send_email(subject, receiver_list, msg)
    #                 mail.sent = True
    #             # 如果是当天的请求
    #             else:
    #                 # 如果这个ip不在当天的字典里，说明当天没有请求过，必发邮件
    #                 if ip not in in_time_alarm[date]:
    #                     # 记录ip的发件时间
    #                     in_time_alarm[date][ip] = now.hour
    #                     send_email(subject, receiver_list, msg)
    #                     mail.sent = True
    #                 # 如果这个ip在当天的字典里，判断是否是同一个点
    #                 else:
    #                     # 如果不是同一个点，说明之前的记录是9点的，现在是17点，再发一次
    #                     if now.hour != in_time_alarm[date][ip]:
    #                         in_time_alarm[date][ip] = now.hour
    #                         send_email(subject, receiver_list, msg)
    #                         mail.sent = True
    #                     # 如果是同一个点，说明之前的记录是9点，现在还是9点，或之前的记录是17点，现在还是17点，不处理
    #                     # else:
    #                     #     pass
    #         db.session.add(mail)
    #         db.session.commit()
    #         return {'code': 1, 'message': '成功'}
    #         # 不是9或17点的请求，直接忽略
    #         # else:
    #         #     pass
    #     elif rule_name == '1小时内不重复':
    #         if ip not in period_alarm:
    #             period_alarm[ip] = now
    #             send_email(subject, receiver_list, msg)
    #             mail.sent = True
    #         else:
    #             if now - period_alarm[ip] > timedelta(hours=1):
    #                 period_alarm[ip] = now
    #                 send_email(subject, receiver_list, msg)
    #                 mail.sent = True
    #         db.session.add(mail)
    #         db.session.commit()
    #         return {'code': 1, 'message': '成功'}
    #     elif rule_name == '积累1小时':
    #         # 当前时间不在字典中
    #         if now.hour not in per_hour_alarm:
    #             # 字典不为空，说明有上一个小时的消息待发
    #             if per_hour_alarm is not None:
    #                 # 取 ip-消息列表的临时字典
    #                 temp_dict = list(per_hour_alarm.values())[0]
    #                 # 遍历临时字典，发送邮件
    #                 for ip, message_list in temp_dict.items():
    #                     # 换行分割同IP积累的消息
    #                     message = '\r\n'.join(message_list)
    #                     send_email(subject, receiver_list, message)
    #                     mail.sent = True
    #                 # 清空字典
    #                 per_hour_alarm.clear()
    #             # 初始化k-list字典, 讲此刻的时间记录，等待下一个整点数
    #             d = defaultdict(list)
    #             per_hour_alarm[now.hour] = d[ip].append(msg)
    #         else:
    #             per_hour_alarm[now.hour][ip].append(msg)
    #         db.session.add(mail)
    #         db.session.commit()
    #         return {'code': 1, 'message': '成功'}
    #     else:
    #         return {'code': 0, 'message': '邮件规则不存在'}
    # else:
    #     return {'code': 0, 'message': 'ip地址错误,不存在此主机'}
