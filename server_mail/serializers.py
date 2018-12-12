from .models import MailInfo, AlarmRule, MailOperation
from rest_framework import serializers


class MailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailInfo
        fields = '__all__'


class MailOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailOperation
        fields = ('id', 'game', 'receiver', 'created_date')


class AlarmRuleSerializer(serializers.ModelSerializer):
    mailoperation_set = MailOperationSerializer(many=True)
    class Meta:
        model = AlarmRule
        fields = '__all__'