import os
from server_management.models import ServerTable


class BaseRule():
    def __init__(self, data):
        self.data = data
        self._type = data.get('type')
        self.ip = data.get('ip', '')
        self.game = data.get('game', '')
        self.platform = data.get('platform', '')
        self.zone = data.get('zone', '')
        self.gametype = self.game or ServerTable.objects.filter(ipadd=self.ip).first().gametype
        if self.ip:
            self.g_pt_zone = self.get_g_pt_zone()
        self.file = self.get_mail_template()

    def get_g_pt_zone(self):
        server = ServerTable.objects.filter(ipadd=self.ip).first()
        g_pt_zone = server.gametype + '_' + server.ptname + '_' + server.zonename
        return g_pt_zone

    def get_mail_template(self):
        file_dir = os.path.dirname(__file__)
        file_name = 'mail_message\\{0}.txt'.format(self._type)
        file = os.path.join(file_dir, file_name)
        return file



class Recharge(BaseRule):
    def __init__(self, *args, **kwargs):
        super(Recharge, self).__init__(*args, **kwargs)

        self.subject = '[充值告警]' + self.ip
        self.message = self.data.get('message')
        self.orderinfo = self.data.get('orderinfo')

    def generate_subject_and_message(self):
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(gametype=self.gametype, message=self.message, orderinfo=self.orderinfo)
        return self.subject, msg

    def validate_data(self):
        self.message = self.data.get('message')
        self.orderinfo = self.data.get('orderinfo')
        return self.message is not None and self.orderinfo is not None
    # def generate_subject_and_message(self):
    #     subject = '[充值告警]' + self.ip
    #     gametype = self.game
    #     message = self.data.get('message')
    #     orderinfo = self.data.get('orderinfo')
    #     with open(self.file, 'r', encoding='utf8') as f:
    #         msg = f.read().format(gametype=gametype, message=message, orderinfo=orderinfo)
    #     return subject, msg


class ServerPerformance(BaseRule):
    def generate_subject_and_message(self):
        subject = '[服务器性能告警]' + self.ip
        hardware = self.data.get('hardware')
        value = self.data.get('value')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(ip=self.ip, hardware=hardware, value=value)
        return subject, msg


class ProgramDelay(BaseRule):
    def generate_subject_and_message(self):
        subject = '[程序延迟告警]' + self.ip
        message = self.data.get('message')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(g_pt_zone=self.g_pt_zone, message=message)
        return subject, msg


class ProgramCrush(BaseRule):
    def generate_subject_and_message(self):
        subject = '[程序崩溃告警]' + self.ip
        programname = self.data.get('programname')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(ip=self.ip, g_pt_zone=self.g_pt_zone, programname=programname)
        return subject, msg


class AbnormalLogin(BaseRule):
    def generate_subject_and_message(self):
        subject = '[异常登录告警]' + self.ip
        accesslan = self.data.get('accesslan')
        accesshost = self.data.get('accesshost')
        accesswlan = self.data.get('accesswlan')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(ip=self.ip, accesslan=accesslan, accesshost=accesshost, accesswlan=accesswlan)
        return subject, msg


class AbnormalLog(BaseRule):
    def generate_subject_and_message(self):
        subject = '[异常日志告警]' + self.ip
        message = self.data.get('message')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(g_pt_zone=self.g_pt_zone, message=message)
        return subject, msg


class AbnormalGmtools(BaseRule):
    def generate_subject_and_message(self):
        subject = '[gm工具异常告警]' + self.ip
        message = self.data.get('message')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(g_pt_zone=self.g_pt_zone, message=message)
        return subject, msg


class PolicyCheck(BaseRule):
    def generate_subject_and_message(self):
        subject = '[策略检测告警]' + self.ip
        message = self.data.get('message')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(ip=self.ip, message=message)
        return subject, msg


class RegularReport(BaseRule):
    def generate_subject_and_message(self):
        subject = '[常规上报]' + self.ip
        message = self.data.get('message')
        with open(self.file, 'r', encoding='utf8') as f:
            msg = f.read().format(ip=self.ip, message=message)
        return subject, msg


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