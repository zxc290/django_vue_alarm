from .models import User, AppList, ServerTable, SendRule, MailInfo, MailOperation, AlarmRule
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'useridentity', 'emailaddress')


class AppListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppList
        fields = ('gid', 'gname')


class ServerTableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServerTable
        fields = ('idx', 'gametype', 'ipadd')


class SendRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendRule
        fields = '__all__'


class MailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailInfo
        fields = '__all__'


class MailOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailOperation
        fields = ('id', 'game', 'receiver', 'created_date', 'send_rules')
        depth = 1


class AlarmRuleSerializer(serializers.ModelSerializer):
    mailoperation_set = MailOperationSerializer(many=True, read_only=True)
    class Meta:
        model = AlarmRule
        fields = '__all__'