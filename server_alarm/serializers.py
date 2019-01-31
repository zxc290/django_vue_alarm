from .models import User, Alarm, Rule, GameOperation, AppList, ServerTable, MailInfo
from rest_framework import serializers
#
#
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'useridentity', 'emailaddress')


class AlarmSerializer(serializers.ModelSerializer):
    # alarm_rules = SendRuleSerializer(many=True, read_only=True)
    # mailoperation_set = MailOperationSerializer(many=True, read_only=True)
    # mailoperation_set = MailOperationListSerializer(many=True, read_only=True)
    class Meta:
        model = Alarm
        # exclude = ('rules', )
        fields = '__all__'


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ('id', 'send_rule', 'description')


class GameOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameOperation
        fields = '__all__'

# class AppListSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = AppList
#         fields = ('gid', 'gname')
#
#
# class ServerTableSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ServerTable
#         fields = ('idx', 'gametype', 'ipadd')
#
#
# class SendRuleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SendRule
#         fields = '__all__'
#
#
# class MailInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MailInfo
#         fields = '__all__'
#
#
# class MailOperationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MailOperation
#         fields = ('game', 'receiver')
#         # depth = 1
#
#
# class MailOperationListSerializer(serializers.ModelSerializer):
#     # test = serializers.CharField(max_length=100, default='')
#     # sendrule_set = SendRuleSerializer(many=True, read_only=True)
#     mail_operations = SendRuleSerializer(many=True, read_only=True)
#     class Meta:
#         model = MailOperation
#         # fields = '__all__'
#         fields = '__all__'
#
#

