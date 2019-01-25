import json
from datetime import datetime, timedelta
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, AppList, ServerTable, MailInfo, Alarm, MailOperation, Rule
# from .serializers import UserSerializer, AppListSerializer, ServerTableSerializer, MailInfoSerializer, AlarmSerializer, MailOperationSerializer, RuleSerializer
from .mail_distribute import ArgsParser
from .send_mail import async_send_mail
from . import scheduler


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class AppListViewSet(viewsets.ModelViewSet):
#     queryset = AppList.objects.all()
#     serializer_class = AppListSerializer


# class ServerTableViewSet(viewsets.ModelViewSet):
#     queryset = ServerTable.objects.all()
#     serializer_class = ServerTableSerializer
# 
# 
# class MailInfoViewSet(viewsets.ModelViewSet):
#     queryset = MailInfo.objects.all()
#     serializer_class = MailInfoSerializer


# class AlarmViewSet(viewsets.ModelViewSet):
#     queryset = Alarm.objects.all()
#     serializer_class = AlarmSerializer


# class MailOperationViewSet(viewsets.ModelViewSet):
#     queryset = MailOperation.objects.all()
#     serializer_class = MailOperationSerializer


# class RuleViewSet(viewsets.ModelViewSet):
#     queryset = Rule.objects.all()
#     serializer_class = RuleSerializer


# @api_view(['POST'])
# def recharge(request):
#     # data = request.data
#     alarm_type = 'recharge'
#     alarm_rule = Alarm.objects.get(alarm_type=alarm_type)
#     parser = ArgsParser(request.data)
#     if parser.validate_json_data():
#         subject, content = parser.generate_subject_and_message()
#         receiver_mail_list = parser.get_receiver_mail_list()
#         mail_info = MailInfo.objects.create(ip_address=parser.ip, game=parser.gametype, title=subject, content=content)
#         mail_info.mail_types.add(alarm_rule)
#         mail_info_args = [mail_info, ]
#         mail_info_kwargs = {
#             'subject': subject,
#             'message': content,
#             'from_email': settings.DEFAULT_FROM_EMAIL,
#             'recipient_list': ['290704731@qq.com'],
#             'fail_silently': False,
#         }
#
#         send_rule =



@api_view(['POST'])
def deal_alarm(request):
    data = json.loads(request.body)
    # 前端报警类型
    alarm_type = data.get('type')
    # 解析前端
    parser = ArgsParser(data)
    # 解析成功
    if parser.validate_json_data():
        # 生成邮件主题和内容
        subject, content = parser.generate_subject_and_message()
        # 生成收件人列表
        receiver_mail_list = parser.get_receiver_mail_list()
        # 保存邮件信息
        mail_info = MailInfo.objects.create(ip_address=parser.ip, game=parser.gametype, title=subject, content=content)
        mail_info.mail_types.add(parser.alarm_rule)
        # 定义发送邮件参数，传入实例方便修改状态
        mail_info_args = [mail_info, ]
        mail_info_kwargs = {
            'subject': subject,
            'message': content,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': ['290704731@qq.com'],
            'fail_silently': False,
        }

        send_rule = parser.get_send_rule()

        if send_rule == 'immediately':
            old_mail = MailInfo.objects.filter(game=parser.gametype).filter(mail_types=parser.alarm_rule).filter(sent=True).first()
            # 不存在旧邮件，直接发
            if not old_mail:
                async_send_mail(*mail_info_args, **mail_info_kwargs)

            # 存在旧邮件，比较时间差是否大于1小时
            else:
                timedelta_seconds = (mail_info.create_date - old_mail.create_date).seconds
                timedelta_hours = timedelta_seconds // 3600
                if timedelta_hours >= 1:
                    async_send_mail(*mail_info_args, **mail_info_kwargs)

        elif send_rule == '定时9,17点':
            date = datetime.now()
            today_start = date.replace(hour=0, minute=0, second=0)
            tomorrow_start = today_start + timedelta(days=1)
            hour = date.hour
            if hour == 9 or 17:
                old_mail = MailInfo.objects.filter(game=parser.gametype).filter(mail_types=parser.alarm_rule).filter(
                    sent=True).filter(create_date__range=[today_start, tomorrow_start]).first()
                # 今天无此游戏报警的邮件，直接发
                if not old_mail:
                    async_send_mail(*mail_info_args, **mail_info_kwargs)
                else:
                    # 今天有此类游戏的报警,但不是这个时间点的，直接发
                    if old_mail.create_date.hour != hour:
                        async_send_mail(*mail_info_args, **mail_info_kwargs)

        elif send_rule == '积累1小时':
            date = datetime.now()
            # 下个小时的整点发
            run_date = datetime(date.year, date.month, date.day, date.hour) + timedelta(hours=1)
            job_id = parser.gametype + '_' + alarm_type + '_' + str(run_date.hour)

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
        return Response({'code': 1, 'message': '成功'})
    else:
        return Response({'code': 0, 'message': '参数错误'})


    # # 当前报警类型的游戏的邮件类实例化
    # mail_instance = alarm_hash[alarm_type](data)
    # # 验证前端json参数
    # if mail_instance.validate_json_data(*mail_instance.json_args):
    #     # 获取邮件主题和内容
    #     subject, content = mail_instance.generate_subject_and_message(**mail_instance.txt_kwargs)
    #     # 报警规则对象
    #     alarm_rule = mail_instance.alarm_rule
    #     # 报警邮件发送规则
    #     mail_rule = alarm_rule.alarm_rule
    #     receiver_mail_list = mail_instance.get_receiver_mail_list(alarm_type)
    #     # 保存邮件信息
    #     mail_info = MailInfo.objects.create(ip_address=mail_instance.ip, game=mail_instance.gametype, title=subject.split(']')[0].strip('['),
    #                                         content=content)
    #     mail_info.mail_types.add(alarm_rule)
    #     # 定义发送邮件参数，传入实例方便修改状态
    #     mail_info_args = [mail_info, ]
    #     mail_info_kwargs = {
    #         'subject': subject,
    #         'message': content,
    #         'from_email': settings.DEFAULT_FROM_EMAIL,
    #         'recipient_list': ['290704731@qq.com'],
    #         'fail_silently': False,
    #     }
    #
    #     if mail_rule == '即时':
    #         old_mail = MailInfo.objects.filter(game=mail_instance.gametype).filter(mail_types=alarm_rule).filter(sent=True).first()
    #         # 不存在旧邮件，直接发
    #         if not old_mail:
    #             async_send_mail(*mail_info_args, **mail_info_kwargs)
    #
    #         # 存在旧邮件，比较时间差是否大于1小时
    #         else:
    #             timedelta_seconds = (mail_info.create_date - old_mail.create_date).seconds
    #             timedelta_hours = timedelta_seconds // 3600
    #             if timedelta_hours >= 1:
    #                 async_send_mail(*mail_info_args, **mail_info_kwargs)
    #
    #     elif mail_rule == '定时9,17点':
    #         date = datetime.now()
    #         today_start = date.replace(hour=0, minute=0, second=0)
    #         tomorrow_start = today_start + timedelta(days=1)
    #         hour = date.hour
    #         if hour == 9 or 17:
    #             old_mail = MailInfo.objects.filter(game=mail_instance.gametype).filter(mail_types=alarm_rule).filter(sent=True).filter(
    #                 create_date__range=[today_start, tomorrow_start]).first()
    #             # 今天无此游戏报警的邮件，直接发
    #             if not old_mail:
    #                 async_send_mail(*mail_info_args, **mail_info_kwargs)
    #             else:
    #                 # 今天有此类游戏的报警,但不是这个时间点的，直接发
    #                 if old_mail.create_date.hour != hour:
    #                     async_send_mail(*mail_info_args, **mail_info_kwargs)
    #
    #     elif mail_rule == '积累1小时':
    #         date = datetime.now()
    #         # 下个小时的整点发
    #         run_date = datetime(date.year, date.month, date.day, date.hour) + timedelta(hours=1)
    #         job_id = mail_instance.gametype + '_' + alarm_type + '_' + str(run_date.hour)
    #
    #         # 根据任务id获取任务
    #         sched = scheduler.get_job(job_id)
    #         # 如果有任务存在，追加邮件内容，追加邮件信息实例
    #         if sched:
    #             modified_content = sched.kwargs.get('message') + '\r\n\r\n' + content
    #             mail_info_args.append(mail_info)
    #             mail_info_kwargs['message'] = modified_content
    #             sched.modify(args=mail_info_args, kwargs=mail_info_kwargs)
    #         # 如果任务不存在，新增定时任务
    #         else:
    #             scheduler.add_job(
    #                 func=async_send_mail, trigger='date', run_date=run_date, id=job_id,
    #                 args=mail_info_args, kwargs=mail_info_kwargs
    #             )
    #     return Response({'code': 1, 'message': '成功'})
    # else:
    #     return Response({'code': 0, 'message': '参数错误'})


# @api_view(['POST'])
# def add_rule(request):
#     data = json.loads(request.body).get('params')
#     alarm_description = data.get('alarmType')
#     game = data.get('game')
#     receiver = data.get('receiver')
#     mail_operation = MailOperation.objects.create(game=game, receiver=receiver)
#     alarm_rule = Alarm.objects.filter(description=alarm_description).first()
#     alarm_rule.mailoperation_set.add(mail_operation)
#     alarm_rule.save()
#     msg = {'code':1, 'message': '成功'}
#     return Response(msg)


# @api_view(['POST'])
# def delete_rule(request):
#     data = json.loads(request.body)
#     alarm_id = data.get('alarmId')
#     alarm_rule = Alarm.objects.get(id=alarm_id)
#     mail_operation_id_list = data.get('delArr')
#     mail_operation_list = [MailOperation.objects.get(id=each) for each in mail_operation_id_list]
#     for mail_operation in mail_operation_list:
#         mail_operation.alarms.remove(alarm_rule)
#         mail_operation.delete()
#     # game = data.get('game')
#     # receiver = data.get('receiver')
#     # alarm_id = data.get('alarmId')
#     # alarm_rule = Alarm.objects.get(id=alarm_id)
#     # mail_operation = MailOperation.objects.filter(game=game, receiver=receiver).first()
#     # alarm_rule.mailoperation_set.remove(mail_operation)
#     # mail_operation.delete()
#     msg = {'code': 1, 'message': '成功'}
#     return Response(msg)


# def index(request):
#     return render(request, 'index.html')


class AlarmList(APIView):
    def get(self, request, format=None):
        alarm_rules = Alarm.objects.all()
        alarm_rule_list = []
        for each in alarm_rules:
            alarm_rule_dict = dict()
            alarm_rule_dict['id'] = each.id
            alarm_rule_dict['alarm_type'] = each.type
            alarm_rule_dict['description'] = each.description
            alarm_rule_dict['json_args'] = each.json_args
            alarm_rule_dict['template_kwargs'] = each.template_kwargs
            alarm_rule_list.append(alarm_rule_dict)

        # serializer = AlarmSerializer(alarm_rules, many=True)
        # return Response(serializer.data)
        message = '获取报警规则列表成功'
        return Response({'code': 1, 'message': message, 'alarm_rule_list': alarm_rule_list})

    # def post(self, request, format=None):
    #     serializer = AlarmSerializer(data=request.data)
    #     if serializer.is_valid():
    #         alarm_rule = serializer.save()
    #         description = request.data.get('description')
    #         alarm_rule = Alarm.objects.filter(description=description).first()
    #         alarm_rule.mailoperation_set.add(mail_operation)
    #         alarm_rule.save()
    #         message = '新建邮件规则成功'
    #         return Response({'code': 1, 'message': message})
    #     message = '新建邮件规则失败'
    #     return Response({'code': 0, 'message': message})


class AlarmDetail(APIView):
    def get_object(self, id):
        try:
            return Alarm.objects.get(id=id)
        except MailOperation.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        alarm_rule = self.get_object(id)
        alarm_rule_dict = dict()
        alarm_rule_dict['id'] = alarm_rule.id
        alarm_rule_dict['alarm_type'] = alarm_rule.type
        alarm_rule_dict['description'] = alarm_rule.description
        alarm_rule_dict['json_args'] = alarm_rule.json_args
        alarm_rule_dict['template_kwargs'] = alarm_rule.template_kwargs
        alarm_rule_dict['send_rules'] = alarm_rule.rules.description
        alarm_rule_dict['mailoperation_set'] = []
        mail_operation_list = alarm_rule.mail_operations_alarms.all()

        for each in mail_operation_list:
            mail_operation_dict = dict()
            mail_operation_dict['id'] = each.id
            mail_operation_dict['game'] = each.game
            mail_operation_dict['receiver'] = each.receiver
            mail_operation_dict['created_date'] = each.created_date
            mail_operation_dict['send_rules'] = each.rules.description
            alarm_rule_dict['mailoperation_set'].append(mail_operation_dict)
            # send_rule_description = each.send_rules.description
            # # send_rule_id = each.send_rules
            # # send_rule_description = Rule.objects.get(id=send_rule_id).description
            # each.send_rules = send_rule_description
        # print(alarm_rule_dict)
        message = '获取{0}规则成功'.format(alarm_rule.description)
        return Response({'code': 1, 'message': message, 'alarm_rule_dict': alarm_rule_dict})

        # serializer = AlarmSerializer(alarm_rule)
        # print(serializer.data)
        # alarm_rule_send_rule_id = serializer.data.get('send_rules')
        # alarm_rule_send_rule_description = Rule.objects.get(id=alarm_rule_send_rule_id).description
        # print(alarm_rule_send_rule_description)
        # mail_operation_list = serializer.data.get('mailoperation_set')
        # for each in mail_operation_list:
        #     send_rule_id = each.get('send_rules')
        #     if send_rule_id:
        #         send_rule_description = Rule.objects.get(id=send_rule_id).description
        #         each['send_rules'] = send_rule_description
        #
        # serializer.data['send_rules'] = alarm_rule_send_rule_description
        # print(serializer.data['send_rules'])
        # serializer.data['mailoperation_set'] = mail_operation_list
        # return Response(serializer.data)


class MailOperationList(APIView):
    def get(self, request, format=None):
        mail_operations = MailOperation.objects.all()
        mail_operations_list = []

        for each in mail_operations:
            mail_operations_dict = dict()
            mail_operations_dict['id'] = each.id
            mail_operations_dict['game'] = each.game
            mail_operations_dict['receiver'] = each.receiver
            mail_operations_dict['created_date'] = each.created_date
            mail_operations_dict['send_rules'] = each.rules.description
            mail_operations_list.append(mail_operations_dict)

        message = '获取操作规则列表成功'
        # serializer = MailOperationSerializer(mail_operations, many=True)
        return Response({'code':1, 'message': message, 'mail_operations_list': mail_operations_list})

    def post(self, request, format=None):
        data = request.data
        type = data.get('alarm_type')
        description = data.get('description')
        game = data.get('game')
        receiver = data.get('receiver')
        send_rules = data.get('send_rule')
        try:
            alarm = Alarm.objects.get(type=type)
            rule = Rule.objects.get(description=send_rules)
            mail_operation, created = MailOperation.objects.get_or_create(game=game, receiver=receiver, rules=rule, alarms=alarm)
            # 创建新对象
            if created:
                # alarm = Alarm.objects.get(description=description)
                # alarm.mailoperation_set.add(mail_operation)
                # alarm.save()
                message = '新建邮件规则成功'
                return Response({'code': 1, 'message': message})
            # 已存在旧对象
            else:
                message = '规则已存在，无法重复创建'
                return Response({'code': 0, 'message': message})
        except:
            message = '新建邮件规则失败'
            return Response({'code': 0, 'message': message})

        # serializer = MailOperationSerializer(data=request.data)
        # if serializer.is_valid():
        #     mail_operation = serializer.save()
        #     alarm_description = request.data.get('description')
        #     alarm_rule = Alarm.objects.filter(description=alarm_description).first()
        #     alarm_rule.mailoperation_set.add(mail_operation)
        #     alarm_rule.save()
        #     rule_description = request.data.get('send_rule')
        #     if rule_description:
        #         send_rule = Rule.objects.filter(description=rule_description).first()
        #     else:
        #         send_rule = alarm_rule.send_rules
        #     send_rule.mail_operations.add(mail_operation)
        #     send_rule.save()
        #     message = '新建邮件规则成功'
        #     return Response({'code': 1, 'message': message})
        # message = '新建邮件规则失败'
        # return Response({'code': 0, 'message': message})
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailOperationDetail(APIView):
    def get_object(self, id):
        try:
            return MailOperation.objects.get(id=id)
        except MailOperation.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        mail_operation = self.get_object(id)
        mail_operation_dict = dict()
        mail_operation_dict['id'] = mail_operation.id
        mail_operation_dict['game'] = mail_operation.game
        mail_operation_dict['receiver'] = mail_operation.receiver
        mail_operation_dict['created_date'] = mail_operation.created_date
        mail_operation_dict['send_rules'] = mail_operation.rules.description
        message = '获取{0}规则成功'.format(mail_operation.game + '_' + mail_operation.receiver)

        return Response({'code': 1, 'message': message, 'mail_operation': mail_operation_dict})

    def put(self, request, id, format=None):
        data = request.data
        alarm_type = data.get('alarm_type')
        description = data.get('description')
        game = data.get('game')
        receiver = data.get('receiver')
        send_rules = data.get('send_rule')
        mail_operation = self.get_object(id)
        try:
            rule = Rule.objects.get(description=send_rules)
            mail_operation.game = game
            mail_operation.receiver = receiver
            mail_operation.rules = rule
            mail_operation.save()
            message = '修改邮件规则成功'
            return Response({'code': 1, 'message': message})
        except:
            message = '修改邮件规则失败'
            return Response({'code': 0, 'message': message})



        # serializer = MailOperationSerializer(mail_operation, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     alarm_description = request.data.get('description')
        #     alarm_rule = Alarm.objects.filter(description=alarm_description).first()
        #     rule_description = request.data.get('send_rule')
        #     if rule_description:
        #         send_rule = Rule.objects.filter(description=rule_description).first()
        #     else:
        #         send_rule = alarm_rule.send_rules
        #     mail_operation.send_rules = send_rule
        #     mail_operation.save()
        #     message = '修改邮件规则成功'
        #     return Response({'code': 1, 'message': message})
        # message = '修改邮件规则失败'
        # return Response({'code': 0, 'message': message})

    def delete(self, request, id, format=None):
        mail_operation = self.get_object(id)
        mail_operation.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        message = '删除邮件规则成功'
        return Response({'code': 1, 'message': message})


@api_view(['POST'])
def multi_delete_mail_operations(request):
    if request.method == 'POST':
        delete_id_list = request.data
        delete_mail_operations = MailOperation.objects.filter(id__in=delete_id_list)
        # try:
        for mail_operation in delete_mail_operations:
            mail_operation.delete()
        message = '批量删除邮件规则成功'
        return Response({'code': 1, 'message': message})
        # except:
        #     message = '批量删除邮件规则失败'
        #     return Response({'code': 0, 'message': message})


@api_view(['GET'])
def get_rule_option_data(request):
    all_user = User.objects.all()
    all_game = AppList.objects.all()
    all_rule = Rule.objects.all()

    user_list = []
    for user in all_user:
        user_dict = dict()
        user_dict['userid'] = user.userid
        user_dict['useridentity'] = user.useridentity
        user_dict['emailaddress'] = user.emailaddress
        user_list.append(user_dict)

    game_list = []
    for game in all_game:
        game_dict = dict()
        game_dict['gid'] = game.gid
        game_dict['gname'] = game.gname
        game_list.append(game_dict)

    send_rule_list = []
    for rule in all_rule:
        send_rule_dict = dict()
        send_rule_dict['id'] = rule.id
        send_rule_dict['rule'] = rule.send_rule
        send_rule_dict['description'] = rule.description
        send_rule_list.append(send_rule_dict)

    message = '获取规则选项成功'

    return Response({'code': 1, 'message': message, 'user_list': user_list, 'game_list': game_list, 'send_rule_list': send_rule_list})

