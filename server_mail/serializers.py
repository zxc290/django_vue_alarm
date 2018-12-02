from .models import MailInfo, MailRule, MailOperation
from rest_framework import serializers


class MailInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailInfo
        fields = '__all__'


class MailRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailRule
        fields = '__all__'


class MailOperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailOperation
        fields = '__all__'
