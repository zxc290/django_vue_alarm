import os
import logging
from django.db import connections
from .models import ServerTable, GameOperation, Alarm, User, Rule
from .dbtools import dict_fetchall


logger = logging.getLogger('django')


class ArgsParser():
    def __init__(self, alarm, data):
        self.data = data
        # self._type = data.get('type')
        self.ip = data.get('ip', '')
        self.game = data.get('game', '')
        self.platform = data.get('platform', '')
        self.zone = data.get('zone', '')
        # self.alarm_rule = Alarm.objects.filter(alarm_type=self._type).first()
        self.alarm = alarm
        self.gametype = self.game or ServerTable.objects.filter(ipadd=self.ip).first().gametype
        self.subject = ''
        self.msg = ''
        self.g_pt_zone = self.get_g_pt_zone()
        self.file = self.get_mail_template()

    def validate_json_data(self):
        required_json_list = self.alarm.json_args.split(',')
        if [arg for arg in required_json_list if arg not in self.data]:
            return False
        else:
            return True

    def generate_subject_and_message(self):
        kwargs = dict()
        for key in self.alarm.template_kwargs.split(','):
            kwargs[key] = self.data.get(key) or self.__dict__[key]
        with open(self.file, 'r', encoding='utf8') as f:
            self.msg = f.read().format(**kwargs)
        return self.alarm.description, self.msg

    def get_recipients_and_rule(self):
        if self.alarm.receivers_by_games:
            sql = "SELECT alarm.receivers as alarm_receivers, alarm.rules_id as alarm_send_rule, operation.receivers as game_receivers, " \
                  "operation.rules_id as game_send_rule FROM server_alarm_alarm as alarm JOIN server_alarm_gameoperation as operation " \
                  "ON alarm.id = operation.alarms_id WHERE operation.game='{game}' AND alarm.type='{type}'".format(game=self.gametype, type=self.alarm.type)
            try:
                server_mail_cursor = connections['server_mail'].cursor()
                server_mail_cursor.execute(sql)
                # print(dict_fetchall(server_mail_cursor))
                result = dict_fetchall(server_mail_cursor)[0]
                rule_id = result.get('game_send_rule')
                if rule_id:
                    send_rule = Rule.objects.get(id=rule_id)
                else:
                    send_rule = self.alarm.rules
                receiver_id_list = list(set(result.get('alarm_receivers').split(',') + result.get('game_receivers').split(',')))
                receiver_list = User.objects.filter(userid__in=receiver_id_list)
                recipients = [each.emailaddress for each in receiver_list]
            except Exception as e:
                print(e)
            finally:
                server_mail_cursor.close()
        else:
            send_rule = self.alarm.rules
            receiver_id_list = self.alarm.receivers.split(',')
            receiver_list = User.objects.filter(userid__in=receiver_id_list)
            recipients = [each.emailaddress for each in receiver_list]
            # receiver_name_list = [each.receiver for each in GameOperation.objects.filter(game=self.gametype).filter(alarms=self.alarm_rule).all()]
            # receiver_mail_list = [User.objects.filter(useridentity=name).first().emailaddress for name in receiver_name_list]
        return send_rule, recipients

    # def get_send_rule(self):
    #     if self.gametype:
    #         # print(GameOperation.objects.filter(game=self.gametype).filter(alarms=self.alarm_rule).first().send_rules)
    #         send_rule = GameOperation.objects.filter(game=self.gametype).filter(alarms=self.alarm_rule).first().send_rules.rule
    #     else:
    #         send_rule = self.alarm_rule.send_rules.rule
    #     return send_rule

    def get_g_pt_zone(self):
        if self.game:
            return self.game + '_' + self.platform + '_' + self.zone
        else:
            if self.ip:
                server = ServerTable.objects.filter(ipadd=self.ip).first()
                return server.gametype + '_' + server.ptname + '_' + server.zonename

    def get_mail_template(self):
        file_dir = os.path.dirname(__file__)
        file_name = 'mail_message\\{0}.txt'.format(self.alarm.type)
        file = os.path.join(file_dir, file_name)
        return file


class BaseRule():
    def __init__(self, data):
        self.data = data
        self._type = data.get('type')
        self.ip = data.get('ip', '')
        self.game = data.get('game', '')
        self.platform = data.get('platform', '')
        self.zone = data.get('zone', '')
        self.alarm_rule = Alarm.objects.filter(alarm_type=self._type).first()
        self.gametype = self.game or ServerTable.objects.filter(ipadd=self.ip).first().gametype
        self.subject = ''
        self.msg = ''
        self.g_pt_zone = self.get_g_pt_zone()
        self.file = self.get_mail_template()

    def get_g_pt_zone(self):
        if self.game:
            return self.game + '_' + self.platform + '_' + self.zone
        else:
            if self.ip:
                server = ServerTable.objects.filter(ipadd=self.ip).first()
                return server.gametype + '_' + server.ptname + '_' + server.zonename

    def get_mail_template(self):
        file_dir = os.path.dirname(__file__)
        file_name = 'mail_message\\{0}.txt'.format(self._type)
        file = os.path.join(file_dir, file_name)
        return file

    def validate_json_data(self, *args):
        print([arg for arg in args if arg not in self.data])
        if [arg for arg in args if arg not in self.data]:
            return False
        else:
            return True

    def generate_subject_and_message(self, **kwargs):
        with open(self.file, 'r', encoding='utf8') as f:
            self.msg = f.read().format(**kwargs)
        return self.subject, self.msg
    
    def get_reciever_mail_list(self, alarm_type):
        alarm_rule = Alarm.objects.filter(alarm_type=alarm_type).first()
        receiver_name_list = GameOperation.objects.filter(game=self.gametype).filter(alarms=alarm_rule).all()
        receiver_mail_list = [User.objects.filter(useridentity=name).first().emailaddress for name in receiver_name_list]
        return receiver_mail_list
        

class Recharge(BaseRule):
    def __init__(self, *args, **kwargs):
        super(Recharge, self).__init__(*args, **kwargs)
        self.subject = '[充值告警]' + self.ip
        self.message = self.data.get('message')
        self.orderinfo = self.data.get('orderinfo')
        self.json_args = ('message', 'orderinfo')
        self.txt_kwargs = {'gametype': self.gametype, 'message': self.message, 'orderinfo': self.orderinfo}


class ServerPerformance(BaseRule):
    def __init__(self, *args, **kwargs):
        super(ServerPerformance, self).__init__(*args, **kwargs)
        self.subject = '[服务器性能告警]' + self.ip
        self.hardware = self.data.get('hardware')
        self.value = self.data.get('value')
        self.json_args = ('hardware', 'value')
        self.txt_kwargs = {'ip': self.ip, 'hardware': self.hardware, 'value': self.value}


class ProgramDelay(BaseRule):
    def __init__(self, *args, **kwargs):
        super(ProgramDelay, self).__init__(*args, **kwargs)
        self.subject = '[程序延迟告警]' + self.ip
        self.message = self.data.get('message')
        self.json_args = ('message',)
        self.txt_kwargs = {'g_pt_zone': self.g_pt_zone, 'message': self.message}


class ProgramCrush(BaseRule):
    def __init__(self, *args, **kwargs):
        super(ProgramCrush, self).__init__(*args, **kwargs)
        self.subject = '[程序崩溃告警]' + self.ip
        self.programname = self.data.get('programname')
        self.json_args = ('programname',)
        self.txt_kwargs = {'ip': self.ip, 'g_pt_zone': self.g_pt_zone, 'programname': self.programname}


class AbnormalLogin(BaseRule):
    def __init__(self, *args, **kwargs):
        super(AbnormalLogin, self).__init__(*args, **kwargs)
        self.subject = '[异常登录告警]' + self.ip
        self.accesslan = self.data.get('accesslan')
        self.accesshost = self.data.get('accesshost')
        self.accesswlan = self.data.get('accesswlan')
        self.json_args = ('programname', 'accesslan', 'accesshost', 'accesswlan')
        self.txt_kwargs = {'ip': self.ip, 'accesslan': self.accesslan, 'accesshost': self.accesshost, 'accesswlan': self.accesswlan}


class AbnormalLog(BaseRule):
    def __init__(self, *args, **kwargs):
        super(AbnormalLog, self).__init__(*args, **kwargs)
        self.subject = '[异常日志告警]' + self.ip
        self.message = self.data.get('message')
        self.json_args = ('message',)
        self.txt_kwargs = {'g_pt_zone': self.g_pt_zone, 'message': self.message}


class AbnormalGmtools(BaseRule):
    def __init__(self, *args, **kwargs):
        super(AbnormalGmtools, self).__init__(*args, **kwargs)
        self.subject = '[gm工具异常告警]' + self.ip
        self.message = self.data.get('message')
        self.json_args = ('message',)
        self.txt_kwargs = {'g_pt_zone': self.g_pt_zone, 'message': self.message}


class PolicyCheck(BaseRule):
    def __init__(self, *args, **kwargs):
        super(PolicyCheck, self).__init__(*args, **kwargs)
        self.subject = '[策略检测告警]' + self.ip
        self.message = self.data.get('message')
        self.json_args = ('message',)
        self.txt_kwargs = {'ip': self.ip, 'message': self.message}


class RegularReport(BaseRule):
    def __init__(self, *args, **kwargs):
        super(RegularReport, self).__init__(*args, **kwargs)
        self.subject = '[常规上报]' + self.ip
        self.message = self.data.get('message')
        self.json_args = ('message',)
        self.txt_kwargs = {'ip': self.ip, 'message': self.message}


alarm_hash = {
    'recharge': Recharge,
    'server_performance': ServerPerformance,
    'program_delay': ProgramDelay,
    'program_crush': ProgramCrush,
    'abnormal_login': AbnormalLogin,
    'abnormal_log': AbnormalLog,
    'abnormal_gmtools': AbnormalGmtools,
    'policy_check': PolicyCheck,
    'regular_report': RegularReport,
}
