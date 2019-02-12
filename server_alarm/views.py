import json
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, AppList, ServerTable, MailInfo, Alarm, GameOperation, Rule
from .serializers import UserSerializer, AlarmSerializer, GameOperationSerializer, RuleSerializer
# from .serializers import UserSerializer, AppListSerializer, ServerTableSerializer, MailInfoSerializer, AlarmSerializer, GameOperationSerializer, RuleSerializer
from .mail_distribute import ArgsParser
from .send_mail import async_send_mail
from . import scheduler
from .tokens import verify_token, gen_json_web_token
from .decorators import token_required


logger = logging.getLogger('django')


@api_view(['POST'])
def deal_alarm(request):
    data = request.data
    # 前端报警类型
    type = data.get('type')
    # 获取报警对象
    alarm = Alarm.objects.get(type=type)
    # 解析前端
    parser = ArgsParser(alarm=alarm, data=data)
    # 解析成功
    if parser.validate_json_data():
        logger.info('验证json传入参数成功')
        # 生成邮件主题和内容
        subject, content = parser.generate_subject_and_message()
        logger.info('生成邮件主题和内容')
        # 生成收件人列表和规则
        rule, recipients = parser.get_recipients_and_rule()
        logger.info('生成收件人列表和规则')
        # 保存邮件信息
        mail_info = MailInfo.objects.create(ip_address=parser.ip, game=parser.gametype, title=subject, content=content)
        mail_info.alarms.add(parser.alarm)
        logger.info('保存邮件信息')
        # 定义发送邮件参数，传入实例方便修改状态
        mail_info_args = [mail_info, ]
        mail_info_kwargs = {
            'subject': subject,
            'message': content,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': ['290704731@qq.com'],
            # 'recipient_list': recipients,
            'fail_silently': False,
        }
        # print(recipients)
        # send_rule = parser.get_send_rule()

        if rule.send_rule == 'immediate':
            old_mail = MailInfo.objects.filter(game=parser.gametype).filter(alarms=parser.alarm).filter(sent=True).first()
            # 不存在旧邮件，直接发
            if not old_mail:
                logger.info('无旧邮件，直接发送即时邮件')
                async_send_mail(*mail_info_args, **mail_info_kwargs)

            # 存在旧邮件，比较时间差是否大于1小时
            else:
                timedelta_seconds = (mail_info.create_date - old_mail.create_date).seconds
                timedelta_hours = timedelta_seconds // 3600
                if timedelta_hours >= 1:
                    logger.info('邮件间隔大于1小时，发送即时邮件')
                    async_send_mail(*mail_info_args, **mail_info_kwargs)

        elif rule.send_rule == '9_or_17':
            date = datetime.now()
            today_start = date.replace(hour=0, minute=0, second=0)
            tomorrow_start = today_start + timedelta(days=1)
            hour = date.hour
            if hour == 9 or 17:
                old_mail = MailInfo.objects.filter(game=parser.gametype).filter(alarms=parser.alarm).filter(
                    sent=True).filter(create_date__range=[today_start, tomorrow_start]).first()
                # 今天无此游戏报警的邮件，直接发
                if not old_mail:
                    logger.info('当前无9_17邮件，发送邮件')
                    async_send_mail(*mail_info_args, **mail_info_kwargs)
                else:
                    # 今天有此类游戏的报警,但不是这个时间点的，直接发
                    if old_mail.create_date.hour != hour:
                        logger.info('已有9点邮件，发送17点邮件')
                        async_send_mail(*mail_info_args, **mail_info_kwargs)

        elif rule.send_rule == 'one_hour':
            date = datetime.now()
            # 下个小时的整点发
            run_date = datetime(date.year, date.month, date.day, date.hour) + timedelta(hours=1)
            job_id = parser.gametype + '_' + type + '_' + str(run_date.hour)

            # 根据任务id获取任务
            sched = scheduler.get_job(job_id)
            logger.info('获取定时任务')
            # 如果有任务存在，追加邮件内容，追加邮件信息实例
            if sched:
                modified_content = sched.kwargs.get('message') + '\r\n\r\n' + content
                mail_info_args.append(mail_info)
                mail_info_kwargs['message'] = modified_content
                sched.modify(args=mail_info_args, kwargs=mail_info_kwargs)
                logger.info('追加定时任务信息')
            # 如果任务不存在，新增定时任务
            else:
                scheduler.add_job(
                    func=async_send_mail, trigger='date', run_date=run_date, id=job_id,
                    args=mail_info_args, kwargs=mail_info_kwargs
                )
                logger.info('新增定时任务')
        return Response({'code': 1, 'message': '成功'})
    else:
        return Response({'code': 0, 'message': '参数错误'})


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
    #         alarm_rule.GameOperation_set.add(mail_operation)
    #         alarm_rule.save()
    #         message = '新建邮件规则成功'
    #         return Response({'code': 1, 'message': message})
    #     message = '新建邮件规则失败'
    #     return Response({'code': 0, 'message': message})


class AlarmDetail(APIView):
    def get_object(self, id):
        try:
            return Alarm.objects.get(id=id)
        except GameOperation.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        alarm_rule = self.get_object(id)
        alarm_rule_dict = dict()
        alarm_rule_dict['id'] = alarm_rule.id
        alarm_rule_dict['type'] = alarm_rule.type
        alarm_rule_dict['description'] = alarm_rule.description
        alarm_rule_dict['json_args'] = alarm_rule.json_args
        alarm_rule_dict['template_kwargs'] = alarm_rule.template_kwargs
        alarm_rule_dict['rule_id'] = alarm_rule.rules.id
        alarm_rule_dict['receivers_by_games'] = alarm_rule.receivers_by_games
        alarm_receiver_id_list = [int(id) for id in alarm_rule.receivers.split(',') if alarm_rule.receivers]
        alarm_receivers = User.objects.filter(userid__in=alarm_receiver_id_list)
        serializer = UserSerializer(alarm_receivers, many=True)
        alarm_rule_dict['receivers'] = serializer.data
        alarm_rule_dict['GameOperation_set'] = []
        go_list = alarm_rule.go_alarms.all()

        for each in go_list:
            mail_operation_dict = dict()
            mail_operation_dict['id'] = each.id
            mail_operation_dict['game'] = each.game
            game_receiver_id_list = [int(id) for id in each.receivers.split(',') if each.receivers]
            game_receivers = User.objects.filter(userid__in=game_receiver_id_list)
            serializer = UserSerializer(game_receivers, many=True)
            mail_operation_dict['receivers'] = serializer.data
            mail_operation_dict['created_date'] = each.created_date
            mail_operation_dict['rule_id'] = each.rules.id
            alarm_rule_dict['GameOperation_set'].append(mail_operation_dict)
            # send_rule_description = each.send_rules.description
            # # send_rule_id = each.send_rules
            # # send_rule_description = Rule.objects.get(id=send_rule_id).description
            # each.send_rules = send_rule_description
        # print(alarm_rule_dict)
        message = '获取{0}规则成功'.format(alarm_rule.description)
        return Response({'code': 1, 'message': message, 'alarm_rule_dict': alarm_rule_dict})

    # def put(self, request, id, format=None):
    #     data = request.data
    #     rule_id = data.get('rule_id')
    #     rule = Rule.objects.get(id=rule_id)
    #     alarm_rule = self.get_object(id)
    #     alarm_rule.rules_id = rule_id
    #     alarm_rule.save()
    #
    #     rule_serializer = RuleSerializer(rule)
    #     alarm_serializer = AlarmSerializer(alarm_rule)
    #     alarm_serializer.data['rule'] = rule_serializer.data
    #
    #     # if alarm_serializer.is_valid():
    #     #     alarm_serializer.save()
    #     return Response({'code': 1, 'alarm': alarm_serializer.data})


        # serializer = AlarmSerializer(alarm_rule)
        # print(serializer.data)
        # alarm_rule_send_rule_id = serializer.data.get('send_rules')
        # alarm_rule_send_rule_description = Rule.objects.get(id=alarm_rule_send_rule_id).description
        # print(alarm_rule_send_rule_description)
        # mail_operation_list = serializer.data.get('GameOperation_set')
        # for each in mail_operation_list:
        #     send_rule_id = each.get('send_rules')
        #     if send_rule_id:
        #         send_rule_description = Rule.objects.get(id=send_rule_id).description
        #         each['send_rules'] = send_rule_description
        #
        # serializer.data['send_rules'] = alarm_rule_send_rule_description
        # print(serializer.data['send_rules'])
        # serializer.data['GameOperation_set'] = mail_operation_list
        # return Response(serializer.data)


class GameOperationList(APIView):
    def get(self, request, format=None):
        mail_operations = GameOperation.objects.all()
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
        # serializer = GameOperationSerializer(mail_operations, many=True)
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
            mail_operation, created = GameOperation.objects.get_or_create(game=game, receiver=receiver, rules=rule, alarms=alarm)
            # 创建新对象
            if created:
                # alarm = Alarm.objects.get(description=description)
                # alarm.GameOperation_set.add(mail_operation)
                # alarm.save()
                message = '新建邮件规则成功'
                return Response({'code': 1, 'message': message})
            # 已存在旧对象
            else:
                message = '规则已存在，无法重复创建'
                return Response({'code': 0, 'message': message})
        except Exception as e:
            print(e)
            message = '新建邮件规则失败'
            return Response({'code': 0, 'message': message})

        # serializer = GameOperationSerializer(data=request.data)
        # if serializer.is_valid():
        #     mail_operation = serializer.save()
        #     alarm_description = request.data.get('description')
        #     alarm_rule = Alarm.objects.filter(description=alarm_description).first()
        #     alarm_rule.GameOperation_set.add(mail_operation)
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


class GameOperationDetail(APIView):
    def get_object(self, id):
        try:
            return GameOperation.objects.get(id=id)
        except GameOperation.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        mail_operation = self.get_object(id)
        mail_operation_dict = dict()
        mail_operation_dict['id'] = mail_operation.id
        mail_operation_dict['game'] = mail_operation.game
        mail_operation_dict['receiver'] = mail_operation.receiver
        mail_operation_dict['created_date'] = mail_operation.created_date
        # mail_operation_dict['send_rules'] = mail_operation.rules.description
        mail_operation_dict['send_rules'] = mail_operation.rules.id
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



        # serializer = GameOperationSerializer(mail_operation, data=request.data)
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
        delete_mail_operations = GameOperation.objects.filter(id__in=delete_id_list)
        # try:
        for mail_operation in delete_mail_operations:
            mail_operation.delete()
        message = '批量删除邮件规则成功'
        return Response({'code': 1, 'message': message})
        # except:
        #     message = '批量删除邮件规则失败'
        #     return Response({'code': 0, 'message': message})


@api_view(['GET'])
@token_required
def get_initial_options(request):
    all_user = User.objects.all()
    all_game = AppList.objects.all()
    all_rule = Rule.objects.all()

    users = []
    for user in all_user:
        user_dict = dict()
        user_dict['userid'] = user.userid
        user_dict['useridentity'] = user.useridentity
        user_dict['emailaddress'] = user.emailaddress
        users.append(user_dict)

    games = []
    for game in all_game:
        game_dict = dict()
        game_dict['gid'] = game.gid
        game_dict['gname'] = game.gname
        games.append(game_dict)

    rules = []
    for rule in all_rule:
        rule_dict = dict()
        rule_dict['id'] = rule.id
        rule_dict['rule'] = rule.send_rule
        rule_dict['description'] = rule.description
        rules.append(rule_dict)

    message = '获取规则选项成功'

    return Response({'code': 1, 'message': message, 'users': users, 'games': games, 'rules': rules})


class RuleList(APIView):
    def get(self, request, format=None):
        rule_list = Rule.objects.all()
        rules = []

        for each in rule_list:
            rule_dict = dict()
            rule_dict['id'] = each.id
            rule_dict['send_rule'] = each.send_rule
            rule_dict['description'] = each.description
            rules.append(rule_dict)

        message = '获取发送规则列表成功'
        # serializer = GameOperationSerializer(mail_operations, many=True)
        return Response({'code':1, 'message': message, 'rules': rules})


class UserList(APIView):
    def get(self, request, format=None):
        user_list = User.objects.all()
        users = []

        for each in user_list:
            user_dict = dict()
            user_dict['userid'] = each.userid
            user_dict['useridentity'] = each.useridentity
            users.append(user_dict)

        message = '获取用户列表成功'
        # serializer = GameOperationSerializer(mail_operations, many=True)
        return Response({'code':1, 'message': message, 'users': users})

# @api_view(['POST'])
# def get_send_rule(request):
#     data = request.data
#     alarm_id = data.get('alarmId')
#     game = data.get('game')
#     alarm = Alarm.objects.get(id=alarm_id)
#     game_operation = GameOperation.objects.get(game=game, alarms=alarm)
#
#
#     return Response({'code': 1, 'message': })


@api_view(['PUT'])
@token_required
def update_alarm_rule(request, id):
    try:
        alarm = Alarm.objects.get(id=id)
    except:
        message = '修改默认发送规则失败'
        return Response({'code': 0, 'message': message})
    if request.method == 'PUT':
        data = request.data
        rule_id = data.get('rule_id')
        rule = Rule.objects.get(id=rule_id)
        alarm.rules = rule
        alarm.save()
        serializer = AlarmSerializer(alarm)
        message = '修改默认发送规则成功'
        return Response({'code': 1, 'message': message, 'alarm': serializer.data})


@api_view(['PUT'])
@token_required
def update_alarm_receiver(request, id):
    try:
        alarm = Alarm.objects.get(id=id)
    except:
        message = '修改默认收件人失败'
        return Response({'code': 0, 'message': message})
    if request.method == 'PUT':
        data = request.data
        user_id_list = data.get('user_id_list')
        receivers = ','.join([str(x) for x in user_id_list])
        alarm.receivers = receivers
        alarm.save()
        alarm_serializer = AlarmSerializer(alarm)
        message = '修改默认收件人成功'
        return Response({'code': 1, 'message': message, 'alarm': alarm_serializer.data})


@api_view(['PUT'])
@token_required
def update_game_rule(request, id):
    try:
        game_operation = GameOperation.objects.get(id=id)
    except:
        message = '修改游戏发送规则失败'
        return Response({'code': 0, 'message': message})
    if request.method == 'PUT':
        data = request.data
        rule_id = data.get('rule_id')
        rule = Rule.objects.get(id=rule_id)
        game_operation.rules = rule
        game_operation.save()
        serializer = GameOperationSerializer(game_operation)
        message = '修改游戏发送规则成功'
        return Response({'code': 1, 'message': message, 'game_operation': serializer.data})


@api_view(['PUT'])
@token_required
def update_game_receiver(request, id):
    try:
        game_operation = GameOperation.objects.get(id=id)
    except:
        message = '修改游戏收件人失败'
        return Response({'code': 0, 'message': message})
    if request.method == 'PUT':
        data = request.data
        user_id_list = data.get('user_id_list')
        receivers = ','.join([str(x) for x in user_id_list])
        game_operation.receivers = receivers
        game_operation.save()
        serializer = GameOperationSerializer(game_operation)
        message = '修改游戏收件人成功'
        return Response({'code': 1, 'message': message, 'game_operation': serializer.data})


@api_view(['POST'])
def login(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    now = datetime.now()
    try:
        user = User.objects.get(useridentity=username)
        user.lastlogintime = int(now.timestamp())
        if user.check_password(password):
            permission_result = user.get_user_permission()
            if not permission_result:
                user.save()
                message = '该用户没有此权限'
                logger.info('登录用户无权限')
                return Response({'code': 0, 'message': message})
            else:
                user.failcount = 0
                user.save()

                # permission_dict = get_permission_dict(permission_result)
                user_info = dict()
                user_info['user_id'] = user.userid
                user_info['username'] = user.useridentity
                # user_info['permission'] = permission_dict

                token = gen_json_web_token(user_info)
                message = '登录成功'
                logger.info('登录成功')
                return Response({'code': 1, 'username': username,
                                 'token': token, 'message': message})
        else:
            last_login_time = datetime.fromtimestamp(user.lastlogintime)
            past_time = now - last_login_time
            if past_time > timedelta(hours=1):
                user.failcount = 0
            user.failcount += 1
            user.save()
            if user.failcount >= 5:
                message = '用户冻结中，请稍后重试'
            else:
                message = '密码错误，剩余{0}次尝试次数'.format(str(5 - user.failcount))
            return Response({'code': 0, 'message': message})
    except BaseException as e:
        message = '该用户不存在'
        return Response({'code': 0, 'message': message})