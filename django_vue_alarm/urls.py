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
from server_alarm import views
# from server_alarm.views import ServerTableViewSet, MailInfoViewSet, deal_alarm, MailOperationList, MailOperationDetail, AlarmRuleList, AlarmRuleDetail, multi_delete_mail_operations, get_rule_option_data, recharge

router = routers.DefaultRouter()
# router.include_root_view = False
# router.register('users', UserViewSet)
# router.register('apps', AppListViewSet)
# router.register('servers', views.ServerTableViewSet)
# router.register('mail_info', views.MailInfoViewSet)
# router.register('alarm_rules', AlarmRuleViewSet)
# router.register('mail_operations', MailOperationViewSet)
# router.register('send_rules', SendRuleViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('alarms/', views.AlarmList.as_view()),
    path('alarms/<int:id>/', views.AlarmDetail.as_view()),
    path('mail_operations/', views.GameOperationList.as_view()),
    path('mail_operations/<int:id>/', views.GameOperationDetail.as_view()),
    path('rules/', views.RuleList.as_view()),
    path('users/', views.UserList.as_view()),
    path('get_initial_options/', views.get_initial_options),
    path('delete_multi_rules/', views.multi_delete_mail_operations),
    # path('users/', UserViewSet),
    path('alarm', views.deal_alarm),
    path('update_alarm_rule/<int:id>/', views.update_alarm_rule),
    path('update_alarm_receiver/<int:id>/', views.update_alarm_receiver),
    path('update_game_rule/<int:id>/', views.update_game_rule),
    path('update_game_receiver/<int:id>/', views.update_game_receiver)
    # path('add_rule', add_rule),
    # path('delete_rule', delete_rule),
    # path('alarm_rules/', AlarmRuleList.as_view()),
    # path('alarm_rules/<int:id>/', AlarmRuleDetail.as_view())
    # path('index', index)
]

