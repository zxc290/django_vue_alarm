# from .models import User, AppList, ServerTable, SendRule, MailInfo, MailOperation, AlarmRule
# from rest_framework import serializers
#
#
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('userid', 'useridentity', 'emailaddress')
#
#
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
# class AlarmRuleSerializer(serializers.ModelSerializer):
#     # alarm_rules = SendRuleSerializer(many=True, read_only=True)
#     # mailoperation_set = MailOperationSerializer(many=True, read_only=True)
#     # mailoperation_set = MailOperationListSerializer(many=True, read_only=True)
#     class Meta:
#         model = AlarmRule
#         fields = '__all__'
