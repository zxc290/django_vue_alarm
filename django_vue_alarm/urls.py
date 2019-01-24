"""django_vue_alarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from server_alarm.views import UserViewSet, AppListViewSet, ServerTableViewSet, MailInfoViewSet, SendRuleViewSet, deal_alarm, MailOperationList, MailOperationDetail, AlarmRuleList, AlarmRuleDetail

router = routers.DefaultRouter()
# router.include_root_view = False
router.register('users', UserViewSet)
router.register('apps', AppListViewSet)
router.register('servers', ServerTableViewSet)
router.register('mail_info', MailInfoViewSet)
# router.register('alarm_rules', AlarmRuleViewSet)
# router.register('mail_operations', MailOperationViewSet)
router.register('send_rules', SendRuleViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('alarm_rules/', AlarmRuleList.as_view()),
    path('alarm_rules/<int:id>/', AlarmRuleDetail.as_view()),
    path('mail_operations/', MailOperationList.as_view()),
    path('mail_operations/<int:id>/', MailOperationDetail.as_view()),
    # path('users/', UserViewSet),
    path('alarm', deal_alarm),
    # path('add_rule', add_rule),
    # path('delete_rule', delete_rule),
    # path('alarm_rules/', AlarmRuleList.as_view()),
    # path('alarm_rules/<int:id>/', AlarmRuleDetail.as_view())
    # path('index', index)
]

