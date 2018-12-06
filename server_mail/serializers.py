from .models import MailInfo, AlarmRule, MailOperation
from rest_framework import serializers


class MailInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailInfo
        fields = '__all__'


class AlarmRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AlarmRule
        fields = '__all__'


class MailOperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailOperation
        fields = '__all__'
