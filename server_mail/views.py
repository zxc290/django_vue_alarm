from rest_framework import viewsets
from .models import MailInfo, MailRule, MailOperation
from .serializers import MailInfoSerializer, MailRuleSerializer, MailOperationSerializer


class MailInfoViewSet(viewsets.ModelViewSet):
    queryset = MailInfo.objects.all()
    serializer_class = MailInfoSerializer


class MailRuleViewSet(viewsets.ModelViewSet):
    queryset = MailRule.objects.all()
    serializer_class = MailRuleSerializer


class MailOperationViewSet(viewsets.ModelViewSet):
    queryset = MailOperation.objects.all()
    serializer_class = MailOperationSerializer

