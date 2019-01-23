from threading import Thread
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


def async_send_mail(*args, **kwargs):
    # 修改邮件为已发送
    for mail_info in args:
        mail_info.sent = True
        mail_info.save()
    # 多线程发送
    t = Thread(target=send_mail, kwargs=kwargs)
    t.start()


    # print('123')
    # mail_info.sent = True
    # mail_info.save()

# def async_send_mail(subject, message, sender, receiver, mail_info, fail_silently=False):
#     t = Thread(target=send_mail,
#                kwargs={'subject': subject, 'message': message, 'from_email': sender, 'recipient_list': receiver,
#                        'fail_silently': fail_silently})
#     t.start()
#     print('123')
#     mail_info.sent = True
#     mail_info.save()