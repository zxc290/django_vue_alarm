from .models import MailInfo, AlarmRule, MailOperation, SendRule
from rest_framework import serializers


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
    mailoperation_set = MailOperationSerializer(many=True)
    class Meta:
        model = AlarmRule
        fields = '__all__'