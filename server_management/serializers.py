from .models import AppList, ServerTable
from rest_framework import serializers


class AppListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppList
        fields = ('gid', 'gname')


class ServerTableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServerTable
        fields = ('idx', 'gametype', 'ipadd')